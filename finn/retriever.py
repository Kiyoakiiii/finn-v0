from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


TOKEN_RE = re.compile(r"[a-z0-9]+")

STOPWORDS = {
    "a",
    "an",
    "and",
    "around",
    "been",
    "can",
    "do",
    "for",
    "have",
    "how",
    "i",
    "is",
    "it",
    "me",
    "my",
    "of",
    "the",
    "to",
    "what",
}

SYNONYMS = {
    "sleeping": "sleep",
    "slept": "sleep",
    "stressed": "stress",
    "hydrate": "hydration",
    "hydrated": "hydration",
    "exercising": "exercise",
    "workout": "movement",
    "walking": "walk",
}


@dataclass(frozen=True)
class KnowledgeEntry:
    title: str
    body: str


@dataclass(frozen=True)
class KnowledgeMatch:
    title: str
    snippet: str
    summary: str
    score: float


class LocalKnowledgeRetriever:
    """Dependency-light lexical retriever for a small curated knowledge base."""

    def __init__(self, entries: list[KnowledgeEntry]) -> None:
        self.entries = entries
        self._doc_vectors = [self._vectorize(f"{entry.title} {entry.body}") for entry in entries]

    @classmethod
    def from_markdown(cls, path: str | Path) -> "LocalKnowledgeRetriever":
        markdown = Path(path).read_text(encoding="utf-8")
        return cls(_parse_markdown_sections(markdown))

    def search(self, query: str, top_k: int = 2) -> list[KnowledgeMatch]:
        query_vector = self._vectorize(query)
        scored: list[tuple[float, KnowledgeEntry]] = []

        for entry, doc_vector in zip(self.entries, self._doc_vectors):
            score = _cosine_similarity(query_vector, doc_vector)
            scored.append((score, entry))

        scored.sort(key=lambda item: item[0], reverse=True)

        matches: list[KnowledgeMatch] = []
        for score, entry in scored[:top_k]:
            if score <= 0:
                continue
            matches.append(
                KnowledgeMatch(
                    title=entry.title,
                    snippet=_first_sentence(entry.body),
                    summary=_summarize_entry(entry.body),
                    score=score,
                )
            )
        return matches

    def _vectorize(self, text: str) -> Counter[str]:
        return Counter(_tokenize(text))


def _tokenize(text: str) -> list[str]:
    tokens = []
    for token in TOKEN_RE.findall(text.lower()):
        normalized = SYNONYMS.get(token, token)
        if normalized not in STOPWORDS:
            tokens.append(normalized)
    return tokens


def _parse_markdown_sections(markdown: str) -> list[KnowledgeEntry]:
    entries: list[KnowledgeEntry] = []
    current_title: str | None = None
    current_lines: list[str] = []

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            if current_title and current_lines:
                entries.append(KnowledgeEntry(current_title, "\n".join(current_lines).strip()))
            current_title = line.removeprefix("## ").strip()
            current_lines = []
        elif current_title:
            current_lines.append(raw_line)

    if current_title and current_lines:
        entries.append(KnowledgeEntry(current_title, "\n".join(current_lines).strip()))

    if not entries:
        raise ValueError("Knowledge base must contain at least one '##' section.")
    return entries


def _cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0

    intersection = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in intersection)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


def _first_sentence(text: str) -> str:
    compact = " ".join(text.split())
    parts = re.split(r"(?<=[.!?])\s+", compact)
    return parts[0] if parts else compact


def _summarize_entry(text: str) -> str:
    compact = " ".join(text.split())
    sentences = re.split(r"(?<=[.!?])\s+", compact)
    return " ".join(sentences[:2]).strip()
