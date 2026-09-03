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
    
    def get_candidates(
        self,
        levels: dict[DemonLevel],
        target: int,
        window: int = 5,
    ) -> list[DemonLevel]:
        maximum_position = target + window
        minimum_position = target - window
        
        candidates = []
        
        for level in levels:
            position = level.position
            
            if minimum_position <= position <= maximum_position:
                candidates.append(level)
                
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