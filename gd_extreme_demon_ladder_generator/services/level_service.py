from gd_extreme_demon_ladder_generator.api.aredl_client import AREDLClient
from gd_extreme_demon_ladder_generator.core.models import DemonLevel


class LevelService:
    def __init__(
        self,
        client: AREDLClient,
        levels: list[DemonLevel | dict] | None = None,
    ):
        self.client = client
        self.levels = DemonLevel.normalize_levels(levels) if levels is not None else client.fetch_levels()

    def retrieve_level_data(
        self,
        level_id: int | None = None,
        level_name: str | None = None,
    ) -> DemonLevel | None:
        if (level_id is None) == (level_name is None):
            raise ValueError(
                "Either the Level ID or the Level Name must be provided."
            )

        levels = self.levels or self.client.fetch_levels()
        self.levels = DemonLevel.normalize_levels(levels)

        if level_id is not None:
            level = self.client.find_level_by_id(levels, level_id)
        else:
            assert level_name is not None
            level = self.client.find_level_by_name(levels, level_name.lower())

        if level is None:
            return None

        level_id_value = getattr(level, "level_id", None)
        if level_id_value is None:
            level_id_value = level.get("level_id")

        detailed_level = self.client.fetch_level(level_id_value)
        return None if detailed_level is None else detailed_level