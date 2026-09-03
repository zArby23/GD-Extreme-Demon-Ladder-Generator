import requests


class AREDLClient:
    def __init__(self, base_url: str, timeout: int):
        self.base_url = base_url
        self.timeout = timeout
    def fetch_levels(self):
        """Fetches the list of all rated extreme demons from the AREDL API.

        Returns:
            dict: The JSON response containing the list of extreme demons.
        """
        endpoint = f"{self.base_url}/aredl/levels"
        
        response = requests.get(
            endpoint,
            timeout=self.timeout
        )
        
        response.raise_for_status()
        
        return response.json()
    def get_level_by_id(self, levels: list[dict], level_id: int) -> dict | None:
        """Retrieves a level from the list based on its ID.

        Args:
            levels (list[dict]): The list of levels.
            level_id (int): The ID of the level to retrieve.

        Returns:
            dict | None: The level object if found, otherwise None.
        """
        return next((level for level in levels if level["level_id"] == level_id), None)
    def get_level_by_position(self, levels: list[dict], position: int) -> dict | None:
        """Retrieves a level from the list based on its position.

        Args:
            levels (list[dict]): The list of levels.
            position (int): The position of the level to retrieve.

        Returns:
            dict | None: The level object if found, otherwise None.
        """
        return next((level for level in levels if level.get("position") == position), None)
    def get_level_by_name(self, levels: list[dict], name: str) -> dict | None:
        """Retrieves a level from the list based on its name.

        Args:
            levels (list[dict]): The list of levels.
            name (str): The name of the level to retrieve.

        Returns:
            dict | None: The level object if found, otherwise None.
        """
        return next((level for level in levels if level["name"].lower() == name.lower()), None)