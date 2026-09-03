from dataclasses import dataclass, field
from typing import Any


@dataclass
class Publisher:
    id: str
    global_name: str | None = field(default="Unknown")
    
    @classmethod
    def fromJson(cls, data: dict[str, Any]) -> "Publisher | None":
        if not data:
            return None
        return cls(
            id=data.get("id", ""),
            global_name=data.get("global_name", "Unknown"),
        )

@dataclass
class DemonLevel:
    id: str
    name: str
    position: int
    level_id: int
    gddl_tier: float | None = field(default=0)
    tags: list[str]
    song_id: int
    publisher: Publisher | None
    
    @classmethod
    def fromJson(cls, data: dict[str, Any]) -> "DemonLevel | None":
        if not data:
            return None
        return cls(
            id=data.get("id", ""),
            name=data.get("name", "Unknown"),
            position=data.get("position", ""),
            level_id=data.get("level_id", 0),
            gddl_tier=data.get("gddl_tier", 0),
            tags=data.get("tags", []),
            song_id=data.get("song_id", 0),
            publisher=Publisher.from_json(data.get("publisher", {})),
        )