from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class UserProfile:
    user_id: str
    primary_goal: str
    avg_sleep_hours: float
    stress_level: int
    daily_water_cups: int
    activity_level: str
    preference: str


def load_user_profile(path: str | Path) -> UserProfile:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return UserProfile(
        user_id=data["user_id"],
        primary_goal=data["primary_goal"],
        avg_sleep_hours=float(data["avg_sleep_hours"]),
        stress_level=int(data["stress_level"]),
        daily_water_cups=int(data["daily_water_cups"]),
        activity_level=data["activity_level"],
        preference=data["preference"],
    )
