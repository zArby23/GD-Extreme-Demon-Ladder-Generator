import requests


class AREDLClient:
    def __init__(self, base_url: str, timeout: int):
        self.base_url = base_url
        self.timeout = timeout
    def _get_request(self, endpoint: str):
        response = requests.get(
            endpoint,
            timeout=self.timeout
        )
        
        response.raise_for_status()
        
        return response
    def fetch_levels(self):
        """Fetches the list of all rated extreme demons from the AREDL API.

        Returns:
            dict: The JSON response containing the list of extreme demons.
        """
        endpoint = f"{self.base_url}/aredl/levels"
        
        return self._get_request(endpoint).json()
    def fetch_level(self, level_id: int) -> dict | None:
        """Retrieves a level from the list based on its ID.

        Args:    
            level_id (int): The ID of the level to retrieve.

        Returns:
            dict | None: The level object if found, otherwise None.
        """
        
        endpoint = f"{self.base_url}/aredl/levels/{level_id}"
        return self._get_request(endpoint).json()
    def find_level_by_id(self, levels: list[dict], level_id: int) -> dict | None:
        """Retrieves a level from the list based on its ID.

        Args:
            levels (list[dict]): The list of levels.
            level_id (int): The ID of the level to retrieve.

        Returns:
            dict | None: The level object if found, otherwise None.
        """
        return next((level for level in levels if level.get("level_id") == level_id), None)
    def find_level_by_position(self, levels: list[dict], position: int) -> dict | None:
        """Retrieves a level from the list based on its position.

        Args:
            levels (list[dict]): The list of levels.
            position (int): The position of the level to retrieve.

        Returns:
            dict | None: The level object if found, otherwise None.
        """
        return next((level for level in levels if level.get("position") == position), None)
    def find_level_by_name(self, levels: list[dict], name: str) -> dict | None:
        """Retrieves a level from the list based on its name.

        Args:
            levels (list[dict]): The list of levels.
            name (str): The name of the level to retrieve.

        Returns:
            dict | None: The level object if found, otherwise None.
        """
        return next((level for level in levels if level["name"].lower() == name.lower()), None)
    def find_publisher_by_id(self, levels: list[dict], publisher_id: str) -> dict | None:
        """Retrieves a publisher from the list based on its ID.

        Args:
            levels (list[dict]): The list of levels.
            publisher_id (str): The ID of the publisher to retrieve.

        Returns:
            dict | None: The publisher object if found, otherwise None.
        """
        return next((level for level in levels if level["publisher"]["id"] == publisher_id), None)