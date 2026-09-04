from gd_extreme_demon_ladder_generator.core.candidate_scoring import CandidateScoring
from gd_extreme_demon_ladder_generator.core.models import DemonLevel


class CandidateSelector:
    @staticmethod
    def select_best_candidate(
        candidates: list[DemonLevel],
        previous: DemonLevel,
        target: DemonLevel
    ) -> DemonLevel | None:
        
        valid_candidates = []
        
        previous_position = previous.get("position", 0)
        
        for candidate in candidates:
            candidate_position = candidate.get("position", 0)
            
            if candidate_position >= previous_position:
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