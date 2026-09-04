import math

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
    
    @staticmethod
    def get_candidates(
        levels: list[DemonLevel],
        target: int,
        window: int = 5,
    ) -> list[DemonLevel]:
        """Get levels within a window of the target position.

        Args:
            levels (list[DemonLevel]): The list of levels.
            target (int): The target position.
            window (int, optional): The window size. Defaults to 5.

        Returns:
            list[DemonLevel]: A list of levels within the window.
        """
        maximum_position = target + window
        minimum_position = target - window

        candidates = []

        candidates.extend(
            level
            for level in levels
            if minimum_position <= level.position <= maximum_position
        )
        return candidates
    
    def build(
        self,
        start: DemonLevel,
        target: DemonLevel,
        steps: int,
        windows: int = 5,
    ) -> list[DemonLevel]:
        
        positions = self.generate_log_positions(
            start.position,
            target.position,
            steps,
        )
        
        ladder = []
        
        for position in positions:
            candidates = self.get_candidates(
                self.levels,
                position,
                windows,
            )
            
            if not candidates:
                continue
            
            candidate = min(
                candidates,
                key=lambda level: abs(level.position - position),
            )
            
            ladder.append(candidate)
        
        return ladder