from dataclasses import dataclass, field
from typing import Any


@dataclass
class DemonLevel:
    id: str
    name: str
    position: int
    level_id: int
    gddl_tier: float | None = field(default=0)
    tags: list[str] | None = field(default_factory=list)
    song_id: int | None = field(default=0)
    publisher: str | None = field(default="")

    @staticmethod
    def coerce(level: "DemonLevel | dict[str, Any] | None") -> "DemonLevel | None":
        if level is None:
            return None

        if isinstance(level, DemonLevel):
            return level

        return DemonLevel.from_json(level)

    @classmethod
    def normalize_levels(
        cls,
        levels: list["DemonLevel | dict[str, Any]"] | None,
    ) -> list["DemonLevel"]:
        normalized: list[DemonLevel] = []

        for level in levels or []:
            candidate = cls.coerce(level)
            if candidate is not None:
                normalized.append(candidate)

        return normalized
    
    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "DemonLevel | None":
        if not data:
            return None
        
        publisher = data.get("publisher") or {}
        if isinstance(publisher, dict):
            publisher_name = publisher.get("global_name", "")
        else:
            publisher_name = str(publisher)
        
        return cls(
            id=data.get("id", ""),
            name=data.get("name", "Unknown"),
            position=data.get("position", 0),
            level_id=data.get("level_id", 0),
            gddl_tier=data.get("gddl_tier", 0),
            tags=data.get("tags", []),
            song_id=data.get("song", 0),
            publisher=publisher_name,
        )