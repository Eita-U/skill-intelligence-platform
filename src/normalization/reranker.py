from sentence_transformers import CrossEncoder

from src.models.skill import Skill

class MiniLMReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, candidates: list[Skill], include_description: bool = False) -> list[tuple[Skill, float]]:
        """
        Rerank the candidates based on their relevance to the query.

        Args:
            query: The query string.
            candidates: A list of Skill objects to be reranked.
            include_description: Whether to include the skill description in the reranking.

        Returns:
            A list of tuples containing the Skill object and its corresponding score,
            sorted in descending order of relevance.
        """
        if not candidates:
            return []
        
        candidate_texts = [
            skill.preferred_label
            if not include_description
            else f"{skill.preferred_label}. {skill.description}"
            for skill in candidates
        ]
        
        scores = self.model.predict([(query, text) for text in candidate_texts])

        ranked_candidates = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
        return ranked_candidates
    
class BGEReranker:
    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, candidates: list[Skill], include_description: bool = False) -> list[tuple[Skill, float]]:
        """
        Rerank the candidates based on their relevance to the query.

        Args:
            query: The query string.
            candidates: A list of Skill objects to be reranked.
            include_description: Whether to include the skill description in the reranking.

        Returns:
            A list of tuples containing the Skill object and its corresponding score,
            sorted in descending order of relevance.
        """
        if not candidates:
            return []
        
        candidate_texts = [
            skill.preferred_label
            if not include_description
            else f"{skill.preferred_label}. {skill.description}"
            for skill in candidates
        ]
        
        scores = self.model.predict([(query, text) for text in candidate_texts])

        ranked_candidates = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
        return ranked_candidates