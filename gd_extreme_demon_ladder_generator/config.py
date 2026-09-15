import os


AREDL_BASE_URL = os.getenv("AREDL_BASE_URL", "https://api.aredl.net/v2/api")
REQUEST_TIMEOUT = int(os.getenv("AREDL_REQUEST_TIMEOUT", "10"))

GAMEPLAY_WEIGHT = float(os.getenv("GAMEPLAY_WEIGHT", "5"))
VEHICLE_WEIGHT = float(os.getenv("VEHICLE_WEIGHT", "4"))
LENGTH_WEIGHT = float(os.getenv("LENGTH_WEIGHT", "3"))
NERVE_CONTROL_WEIGHT = float(os.getenv("NERVE_CONTROL_WEIGHT", "3"))
VERSION_WEIGHT = float(os.getenv("VERSION_WEIGHT", "2"))