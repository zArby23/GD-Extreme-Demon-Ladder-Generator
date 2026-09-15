import math

from gd_extreme_demon_ladder_generator.core.candidate_selector import CandidateSelector
from gd_extreme_demon_ladder_generator.core.models import DemonLevel


class LadderBuilder:
    def __init__(self, levels: list[DemonLevel]):
        self.levels = levels
    
    def generate_log_positions(
        self,
        start: int,
        target: int,
        steps: int,
    ) -> list[int]:
        """Generate a list of positions between start and target

        Args:
            start (int): The position of the starting level.
            target (int): The position of the target level.
            steps (int): Number of steps for the ladder.

        Returns:
            list[int]: A list of positions.
        """
        if start <= 0 or target <=0:
            raise ValueError("The positions of the levels must be greater than 0.")
        if steps <= 0:
            raise ValueError("The number of steps must be greater than 0.")
        
        start_log = math.log(start)
        target_log = math.log(target)
        
        positions = []
        
        for i in range(steps+1):
            t = i/steps
            
            log_position = start_log + (
                target_log - start_log
            ) * t
            
            position = math.exp(log_position)
            
            positions.append(round(position))
            
        return positions
    
    def build(
        self,
        start: DemonLevel,
        target: DemonLevel,
        steps: int,
        window: int = 5,
    ) -> list[DemonLevel]:
        if start.position < target.position:
            raise ValueError("The starting level must be lower in the list than the target level.")

        if window < 0:
            raise ValueError("The window between levels must be positive.")

        positions = self.generate_log_positions(
            start.position,
            target.position,
            steps,
        )

        ladder = [start]
        previous = start
        used_ids = {start.level_id, target.level_id}

        for position in positions:
            candidates = CandidateSelector.get_candidates(
                self.levels,
                position,
                window,
            )
            unused_candidates = [
                candidate
                for candidate in candidates
                if candidate.level_id not in used_ids
            ]

            best_candidate = CandidateSelector.select_best_candidate(
                unused_candidates,
                previous,
                target,
            )

            if best_candidate is None:
                print(
                    f"No mejor candidato encontrado para la posición {position}; "
                    "se conserva el valor previo."
                )
                continue

            ladder.append(best_candidate)
            previous = best_candidate
            used_ids.add(best_candidate.level_id)

        if ladder[-1].level_id != target.level_id:
            ladder.append(target)

        return ladder