from gd_extreme_demon_ladder_generator.api.aredl_client import AREDLClient
from gd_extreme_demon_ladder_generator.config import AREDL_BASE_URL, REQUEST_TIMEOUT
from gd_extreme_demon_ladder_generator.core.ladder_builder import LadderBuilder
from gd_extreme_demon_ladder_generator.services.level_service import LevelService


def _read_int(prompt: str, default: int) -> int:
	value = input(f"{prompt} [{default}]: ").strip()
	return int(value) if value else default


def _retrieve_level(service: LevelService, value: str):
	if value.isdigit():
		return service.retrieve_level_data(level_id=int(value))
	return service.retrieve_level_data(level_name=value)


def main() -> None:
	client = AREDLClient(AREDL_BASE_URL, REQUEST_TIMEOUT)
	service = LevelService(client)

	start_input = input("Write the start level ID or name: ").strip()
	target_input = input("Write the target level ID or name: ").strip()
	steps = _read_int("Write the number of steps for the ladder", 20)
	window = _read_int("Write the search window for candidates", 5)

	start = _retrieve_level(service, start_input)
	target = _retrieve_level(service, target_input)

	if start is None or target is None:
		raise RuntimeError(
			f"No se encontraron los niveles solicitados: start={start_input}, target={target_input}"
		)

	ladder = LadderBuilder(service.levels).build(
		start=start,
		target=target,
		steps=steps,
		window=window,
	)

	for index, level in enumerate(ladder):
		print(f"{index:02d} | #{level.position:4} | {level.name} | Tier {level.gddl_tier}")


if __name__ == "__main__":
	main()
