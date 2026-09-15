from dataclasses import asdict

from django.conf import settings
from django.core.cache import cache

from gd_extreme_demon_ladder_generator.api.aredl_client import AREDLClient
from gd_extreme_demon_ladder_generator.core.ladder_builder import LadderBuilder
from gd_extreme_demon_ladder_generator.core.models import DemonLevel
from gd_extreme_demon_ladder_generator.services.level_service import LevelService


def _level_payload(level: DemonLevel, position: int) -> dict:
    data = asdict(level)
    data["position"] = position
    return data


def get_level_service() -> LevelService:
    cached_levels = cache.get("aredl:levels")
    client = AREDLClient(
        settings.AREDL_BASE_URL,
        settings.AREDL_REQUEST_TIMEOUT,
    )
    if cached_levels is None:
        service = LevelService(client)
        cache.set(
            "aredl:levels",
            [asdict(level) for level in service.levels],
            timeout=settings.AREDL_CACHE_TTL,
        )
        return service
    return LevelService(client, levels=cached_levels)


def clear_level_cache() -> None:
    cache.delete("aredl:levels")


def _find_level(service: LevelService, value: str) -> DemonLevel | None:
    if value.isdigit():
        return service.retrieve_level_data(level_id=int(value))
    return service.retrieve_level_data(level_name=value)


def generate_ladder(
    *,
    start: str,
    target: str,
    steps: int,
    window: int,
) -> tuple[list[dict], list[str]]:
    service = get_level_service()
    start_level = _find_level(service, start)
    target_level = _find_level(service, target)

    missing = []
    if start_level is None:
        missing.append(f"start={start}")
    if target_level is None:
        missing.append(f"target={target}")
    if missing:
        raise LookupError(f"Requested levels were not found: {', '.join(missing)}")

    ladder = LadderBuilder(service.levels).build(
        start=start_level,
        target=target_level,
        steps=steps,
        window=window,
    )
    warnings = [
        "Some positions did not have a suitable candidate."
    ] if len(ladder) < steps + 1 else []
    return (
        [_level_payload(level, index) for index, level in enumerate(ladder)],
        warnings,
    )
