from gd_extreme_demon_ladder_generator.api.aredl_client import AREDLClient
from gd_extreme_demon_ladder_generator.core.models import DemonLevel


class LevelService:
    def __init__(self, client: AREDLClient):
        self.client = client

    def retrieve_level_data(
        self,
        level_id: int | None = None,
        level_name: str | None = None,
    ) -> DemonLevel | None:

        if (level_id is None) == (level_name is None):
            raise ValueError(
                "Either the Level ID or the Level Name must be provided."
            )

        levels = self.client.fetch_levels()

        if level_id is not None:
            level = self.client.find_level_by_id(
                levels,
                level_id,
            )
        else:
            level = self.client.find_level_by_name(
                levels,
                level_name.lower(),
            )

        if level is None:
            return None

        detailed_level = self.client.fetch_level(
            level["level_id"]
        )

        return DemonLevel.from_json(detailed_level)