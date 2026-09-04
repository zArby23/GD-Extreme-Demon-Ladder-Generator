from gd_extreme_demon_ladder_generator.config import (
    GAMEPLAY_WEIGHT,
    LENGTH_WEIGHT,
    NERVE_CONTROL_WEIGHT,
    VEHICLE_WEIGHT,
    VERSION_WEIGHT,
)
from gd_extreme_demon_ladder_generator.core.models import DemonLevel

GAMEPLAY_TAGS = {
    "2P",
    "Circles",
    "Clicksync",
    "Fast-Paced",
    "Timings",
    "Chokepoints",
    "Learny",
    "Memory",
    "High CPS",
    "Gimmicky",
    "Flow",
    "Slow-Paced",
    "Bossfight",
    "Mirror",
    "Duals",
    "Overall",
    "Old Swing",
    "New Swing"
}
VEHICLE_TAGS = {
    "Cube",
    "Ship",
    "Ball",
    "UFO",
    "Wave",
    "Robot",
    "Spider",
    "Old Swing",
    "New Swing"
}
LENGTH_TAGS = {
    "Medium",
    "Long",
    "XL",
    "XXL",
    "XXL+"
}
VERSION_TAGS = {
    "1.5",
    "1.6",
    "1.6PS",
    "1.7",
    "1.8",
    "1.9",
    "1.9PS",
    "2.0",
    "2.1",
    "2.2",
}
LENGTH_VALUES = {
    "Medium": 0,
    "Long": 1,
    "XL": 2,
    "XXL": 3,
    "XXL+": 4,
}
VERSION_VALUES = {
    "1.5": 0,
    "1.6": 1,
    "1.6ps": 1,
    "1.7": 2,
    "1.8": 3,
    "1.9": 4,
    "1.9ps": 4,
    "2.0": 5,
    "2.1": 6,
    "2.2": 7,
}

class CandidateScoring:
    @staticmethod
    def get_tags(level: DemonLevel) -> set[str]:
        if level is None:
            return set()
        
        if isinstance(level, dict):
            level = DemonLevel.from_json(level)
        return set(level.tags or [])
    @staticmethod
    def get_gameplay_tags(level: DemonLevel) -> set[str]:
        return (
            CandidateScoring.get_tags(level)
            & GAMEPLAY_TAGS
        )
    @staticmethod
    def get_vehicle_tags(level: DemonLevel) -> set[str]:
        return (
            CandidateScoring.get_tags(level)
            & VEHICLE_TAGS
        )
    @staticmethod
    def get_length(level: DemonLevel) -> int | None:
        tags = CandidateScoring.get_tags(level)

        return next((value for tag, value in LENGTH_VALUES.items() if tag in tags), None)
    @staticmethod
    def get_version(level: DemonLevel) -> int | None:
        tags = CandidateScoring.get_tags(level)
        
        return next((value for tag, value in VERSION_VALUES.items() if tag in tags), None)
    @staticmethod
    def has_nerve_control(level: DemonLevel) -> bool:
        return "Nerve Control" in CandidateScoring.get_tags(level)
    @staticmethod
    def calculate_tag_transition_score(
        previous: set[str],
        candidate: set[str],
        target: set[str]
    ) -> float:
        
        if not previous and not target:
            return 1.0
        
        continuity = (
            len(candidate & previous)
            / len(previous)
            if previous
            else 0.0
        )
        
        target_similarity = (
            len(candidate & target)
            / len(target)
            if target
            else 0.0
        )
        
        new_target = target - previous
        
        bridge = (
            len(candidate & new_target)
            / len(new_target)
            if new_target
            else 0.0
        )
        return (
            continuity * 0.4
            + target_similarity * 0.4
            + bridge * 0.2
        )
    @staticmethod
    def calculate_gameplay_score(
        previous: DemonLevel,
        candidate: DemonLevel,
        target: DemonLevel 
    ) -> float:
        
        return CandidateScoring.calculate_tag_transition_score(
            CandidateScoring.get_gameplay_tags(previous),
            CandidateScoring.get_gameplay_tags(candidate),
            CandidateScoring.get_gameplay_tags(target),
        )
    @staticmethod
    def calculate_vehicle_score(
        previous: DemonLevel,
        candidate: DemonLevel,
        target: DemonLevel,
    ) -> float:

        return CandidateScoring.calculate_tag_transition_score(
            CandidateScoring.get_vehicle_tags(previous),
            CandidateScoring.get_vehicle_tags(candidate),
            CandidateScoring.get_vehicle_tags(target),
        )
    @staticmethod
    def calculate_length_score(
        candidate: DemonLevel,
        target: DemonLevel,
    ) -> float:

        candidate_length = CandidateScoring.get_length(candidate)
        target_length = CandidateScoring.get_length(target)

        if candidate_length is None or target_length is None:
            return 0.0

        distance = abs(candidate_length - target_length)

        max_distance = len(LENGTH_VALUES) - 1

        return 1 - (distance / max_distance)
    @staticmethod
    def calculate_version_score(
        candidate: DemonLevel,
        target: DemonLevel,
    ) -> float:

        candidate_version = CandidateScoring.get_version(candidate)
        target_version = CandidateScoring.get_version(target)

        if candidate_version is None or target_version is None:
            return 0.0

        distance = abs(candidate_version - target_version)

        max_distance = max(VERSION_VALUES.values())

        return 1 - (distance / max_distance)
    @staticmethod
    def calculate_nerve_control_score(
        candidate: DemonLevel,
        target: DemonLevel,
    ) -> float:

        target_has_nerve = CandidateScoring.has_nerve_control(target)

        if not target_has_nerve:
            return 1.0

        if CandidateScoring.has_nerve_control(candidate):
            return 1.0

        candidate_length = CandidateScoring.get_length(candidate)
        target_length = CandidateScoring.get_length(target)

        if candidate_length is None or target_length is None:
            return 0.0

        distance = abs(candidate_length - target_length)
        max_distance = len(LENGTH_VALUES) - 1

        return 1 - (distance / max_distance)
    @staticmethod
    def calculate_transition_score(
        previous: DemonLevel,
        candidate: DemonLevel,
        target: DemonLevel,
    ) -> float:
        
        gameplay_score = CandidateScoring.calculate_gameplay_score(previous, candidate, target)
        vehicle_score = CandidateScoring.calculate_vehicle_score(previous, candidate, target)
        length_score = CandidateScoring.calculate_length_score(candidate, target)
        version_score = CandidateScoring.calculate_version_score(candidate, target)
        nerve_control_score = CandidateScoring.calculate_nerve_control_score(candidate, target)
        
        total_weight = (
            GAMEPLAY_WEIGHT
            + VEHICLE_WEIGHT
            + LENGTH_WEIGHT
            + NERVE_CONTROL_WEIGHT
            + VERSION_WEIGHT
        )
        
        weighted_score = (
            gameplay_score * GAMEPLAY_WEIGHT
            + vehicle_score * VEHICLE_WEIGHT
            + length_score * LENGTH_WEIGHT
            + nerve_control_score * NERVE_CONTROL_WEIGHT
            + version_score * VERSION_WEIGHT
        )
        
        return weighted_score / total_weight
