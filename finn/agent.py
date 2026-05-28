from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from finn.retriever import KnowledgeMatch, LocalKnowledgeRetriever
from finn.safety import SafetyDecision, route_message
from finn.user_context import UserProfile, load_user_profile


@dataclass(frozen=True)
class AgentAnswer:
    response: str
    category: str
    sources: list[KnowledgeMatch]
    confidence: float


class FinnAgent:
    """Small retrieval-grounded wellness agent for the v0 prototype."""

    def __init__(self, kb_path: str | Path, user_profile_path: str | Path) -> None:
        self.retriever = LocalKnowledgeRetriever.from_markdown(kb_path)
        self.user_profile = load_user_profile(user_profile_path)

    def answer(self, message: str) -> AgentAnswer:
        safety = route_message(message)
        if not safety.allowed:
            return AgentAnswer(
                response=safety.message,
                category=safety.category,
                sources=[],
                confidence=1.0,
            )

        matches = self.retriever.search(message, top_k=2)
        if not matches or matches[0].score < 0.08:
            return AgentAnswer(
                response=self._clarify_response(),
                category="needs_clarification",
                sources=[],
                confidence=0.3,
            )

        response = self._compose_response(message, matches, self.user_profile, safety)
        return AgentAnswer(
            response=response,
            category="wellness_answer",
            sources=matches,
            confidence=min(matches[0].score, 1.0),
        )

    def _compose_response(
        self,
        message: str,
        matches: list[KnowledgeMatch],
        profile: UserProfile,
        safety: SafetyDecision,
    ) -> str:
        top = matches[0]
        topic = top.title.lower()
        next_step = self._next_step_for_topic(topic, profile)
        personalization = self._personalization_for_topic(topic, profile)

        response_parts = [
            f"Based on Finn's wellness knowledge base, {top.summary}",
        ]

        if personalization:
            response_parts.append(personalization)

        response_parts.append(f"A good small next step: {next_step}")
        response_parts.append(
            "This is general wellness guidance, not medical advice. If symptoms feel severe, persistent, or worrying, it is best to talk with a qualified professional."
        )

        source_titles = ", ".join(match.title for match in matches)
        response_parts.append(f"Sources: {source_titles}.")

        return "\n\n".join(response_parts)

    def _personalization_for_topic(self, topic: str, profile: UserProfile) -> str:
        if "sleep" in topic:
            return (
                f"Your sample profile shows an average of {profile.avg_sleep_hours} hours of sleep and a goal to {profile.primary_goal.lower()}, "
                "so I would prioritize consistency before adding more complicated routines."
            )
        if "stress" in topic or "mindfulness" in topic:
            return (
                f"Your sample stress level is {profile.stress_level}/10, so Finn would keep the first step short and repeatable instead of asking for a big lifestyle change."
            )
        if "hydration" in topic:
            return (
                f"Your sample hydration average is {profile.daily_water_cups} cups per day. Finn would use that as a baseline and nudge gradual improvement."
            )
        if "movement" in topic or "activity" in topic:
            return (
                f"Your sample activity level is {profile.activity_level}, so the safest v0 suggestion is a low-friction movement habit."
            )
        if "nutrition" in topic:
            return (
                f"Your sample preference is {profile.preference}, so Finn would suggest a simple option that fits your routine."
            )
        return (
            f"Your current goal is to {profile.primary_goal.lower()}, so Finn would connect the answer back to that goal when possible."
        )

    def _next_step_for_topic(self, topic: str, profile: UserProfile) -> str:
        if "sleep" in topic:
            return "choose one bedtime and wake time for the next three days, then add a 20-minute wind-down routine before bed."
        if "stress" in topic:
            return "try a two-minute breathing reset now, then schedule one short break before your highest-stress part of the day."
        if "hydration" in topic:
            return "add one glass of water after waking and one glass with your first meal, then adjust based on thirst, activity, and weather."
        if "movement" in topic or "activity" in topic:
            return "take a 10-minute walk or do a short mobility routine today, then repeat it at the same time tomorrow."
        if "nutrition" in topic:
            return "build one meal around a protein source, a high-fiber carbohydrate, and a fruit or vegetable."
        if "habit" in topic:
            return "make the habit small enough that it can be done even on a busy day, then attach it to something you already do."
        return "pick one tiny action you can complete today and check whether it helped."

    def _clarify_response(self) -> str:
        return (
            "I may need a little more context to answer safely. Finn is best at sleep, stress, hydration, movement, nutrition, and habit-building questions. "
            "Try asking something like: 'How can I improve my sleep this week?' or 'What is a simple way to manage stress today?'"
        )
