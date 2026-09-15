import requests

from gd_extreme_demon_ladder_generator.core.models import DemonLevel


class AREDLClientError(RuntimeError):
    """Raised when AREDL cannot be reached or returns an invalid response."""


class AREDLClient:
    def __init__(self, base_url: str, timeout: int):
        self.base_url = base_url
        self.timeout = timeout

    @staticmethod
    def _get_value(level: DemonLevel | dict, field: str):
        if isinstance(level, dict):
            return level.get(field)
        return getattr(level, field, None)

    def _get_request(self, endpoint: str):
        try:
            response = requests.get(endpoint, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as error:
            raise AREDLClientError(
                f"AREDL request failed for {endpoint}: {error}"
            ) from error

        return response

    def fetch_levels(self) -> list[DemonLevel]:
        """Fetches the list of all rated extreme demons from the AREDL API."""
        endpoint = f"{self.base_url}/aredl/levels"
        raw_levels = self._get_request(endpoint).json()
        return DemonLevel.normalize_levels(raw_levels)

    def fetch_level(self, level_id: int) -> DemonLevel | None:
        """Retrieves a level from the list based on its ID."""
        endpoint = f"{self.base_url}/aredl/levels/{level_id}"
        raw_level = self._get_request(endpoint).json()
        return DemonLevel.from_json(raw_level)

    def find_level_by_id(
        self,
        levels: list[DemonLevel | dict],
        level_id: int,
    ) -> DemonLevel | dict | None:
        return next(
            (level for level in levels if self._get_value(level, "level_id") == level_id),
            None,
        )

    def find_level_by_position(
        self,
        levels: list[DemonLevel | dict],
        position: int,
    ) -> DemonLevel | dict | None:
        return next(
            (level for level in levels if self._get_value(level, "position") == position),
            None,
        )

    def find_level_by_name(
        self,
        levels: list[DemonLevel | dict],
        name: str,
    ) -> DemonLevel | dict | None:
        normalized_name = name.lower()
        return next(
            (
                level
                for level in levels
                if str(self._get_value(level, "name")).lower() == normalized_name
            ),
            None,
        )

    def find_publisher_by_id(
        self,
        levels: list[DemonLevel | dict],
        publisher_id: str,
    ) -> DemonLevel | dict | None:
        return next(
            (
                level
                for level in levels
                if str(self._get_value(level, "publisher")).lower() == publisher_id.lower()
            ),
            None,
        )