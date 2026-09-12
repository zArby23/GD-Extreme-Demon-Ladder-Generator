from gd_extreme_demon_ladder_generator.core.candidate_scoring import CandidateScoring
from gd_extreme_demon_ladder_generator.core.models import DemonLevel


class CandidateSelector:
    
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
    
    
    @staticmethod
    def select_best_candidate(
        candidates: list[DemonLevel],
        previous: DemonLevel,
        target: DemonLevel
    ) -> DemonLevel | None:
        
        valid_candidates = []
        
        previous_position = previous.position
        
        for candidate in candidates:
            candidate_position = candidate.position
            
            if candidate_position >= previous_position:
                continue
            if candidate.position < target.position:
                continue
            
            valid_candidates.append(candidate)
        
        if not valid_candidates:
            return None
        
        best_candidate = None
        best_score = -1.0
        
        for candidate in valid_candidates:
            score = CandidateScoring.calculate_transition_score(previous, candidate, target)
            
            if score > best_score:
                best_candidate = candidate
                best_score = score
        
        return best_candidate