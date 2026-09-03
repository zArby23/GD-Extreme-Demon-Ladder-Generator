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
    
    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "DemonLevel | None":
        if not data:
            return None
        
        publisher = data.get("publisher",{})
        return cls(
            id=data.get("id", ""),
            name=data.get("name", "Unknown"),
            position=data.get("position", 0),
            level_id=data.get("level_id", 0),
            gddl_tier=data.get("gddl_tier", 0),
            tags=data.get("tags", []),
            song_id=data.get("song_id", 0),
            publisher=publisher.get("global_name", ""),
        )