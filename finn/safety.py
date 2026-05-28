from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    category: str
    message: str


URGENT_PATTERNS = [
    r"\bchest pain\b",
    r"\bcan't breathe\b",
    r"\bcannot breathe\b",
    r"\bheart attack\b",
    r"\bstroke\b",
    r"\boverdose\b",
    r"\bseizure\b",
    r"\bbleeding heavily\b",
    r"\bkill myself\b",
    r"\bsuicide\b",
    r"\bself harm\b",
]

DIAGNOSIS_PATTERNS = [
    r"\bdiagnose\b",
    r"\bdo i have\b",
    r"\bwhat disease\b",
    r"\bwhat condition\b",
    r"\btest result\b",
]

MEDICATION_PATTERNS = [
    r"\bdosage\b",
    r"\bdose\b",
    r"\bmg\b",
    r"\bprescribe\b",
    r"\bshould i take\b",
    r"\bcan i take\b",
    r"\bantibiotic\b",
    r"\bmedication\b",
    r"\bmedicine\b",
    r"\bmelatonin\b",
    r"\bibuprofen\b",
    r"\bssri\b",
]

WELLNESS_TERMS = {
    "sleep",
    "slept",
    "tired",
    "stress",
    "stressed",
    "anxiety",
    "anxious",
    "water",
    "hydrate",
    "hydration",
    "exercise",
    "movement",
    "walk",
    "workout",
    "nutrition",
    "meal",
    "food",
    "habit",
    "routine",
    "mindfulness",
    "breathing",
    "energy",
    "wellness",
    "health",
}

OUT_OF_SCOPE_TERMS = {
    "stock",
    "crypto",
    "bitcoin",
    "code",
    "python",
    "homework",
    "essay",
    "weather",
    "movie",
    "recipe",
    "travel",
}


def route_message(message: str) -> SafetyDecision:
    text = _normalize(message)

    if _matches_any(text, URGENT_PATTERNS):
        return SafetyDecision(
            allowed=False,
            category="urgent_or_crisis",
            message=(
                "I am really sorry you are dealing with that. Finn cannot handle emergencies or crisis situations. "
                "If you might be in immediate danger, call local emergency services now. In the U.S., you can also call or text 988 for crisis support."
            ),
        )

    if _matches_any(text, DIAGNOSIS_PATTERNS):
        return SafetyDecision(
            allowed=False,
            category="diagnosis_request",
            message=(
                "Finn cannot diagnose symptoms or medical conditions. A licensed healthcare professional is the right person to help with that. "
                "I can still share general wellness information, such as sleep, hydration, stress management, movement, or habit-building tips."
            ),
        )

    if _matches_any(text, MEDICATION_PATTERNS):
        return SafetyDecision(
            allowed=False,
            category="medication_request",
            message=(
                "Finn cannot recommend medication, supplement, or dosage decisions. Please check with a licensed healthcare professional or pharmacist. "
                "If you want, I can share general non-medication wellness habits related to sleep, stress, hydration, or movement."
            ),
        )

    if _looks_unrelated(text):
        return SafetyDecision(
            allowed=False,
            category="out_of_scope",
            message=(
                "Finn is focused on general wellness support, so I cannot help much with that topic. "
                "Try asking about sleep, stress, hydration, movement, nutrition, or building healthier routines."
            ),
        )

    return SafetyDecision(allowed=True, category="wellness_candidate", message="")


def _normalize(message: str) -> str:
    return re.sub(r"\s+", " ", message.lower()).strip()


def _matches_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def _looks_unrelated(text: str) -> bool:
    tokens = set(re.findall(r"[a-z0-9]+", text))
    return bool(tokens & OUT_OF_SCOPE_TERMS) and not bool(tokens & WELLNESS_TERMS)
