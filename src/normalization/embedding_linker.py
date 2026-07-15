from src.models.skill import Skill
from src.normalization.embedding_index import EmbeddingIndex

class EmbeddingLinker:
    def __init__(self, embedding_index: EmbeddingIndex):
        self.embedding_index = embedding_index

    def link_skills(self, text: str, top_k: int = 5) -> list[tuple[Skill, float]]:
        """
        Link skills to the embedding index.

        Args:
            text: The text to link.
            top_k: The number of top matches to return.
        """
        if self.embedding_index.embeddings is None:
            raise ValueError("Embedding index has not been built.")

        skill_embedding = self.embedding_index.embedding_model.encode([text])[0]
        print("index shape:", self.embedding_index.embeddings.shape)
        print("query shape:", skill_embedding.shape)
        similarities = self.embedding_index.embeddings @ skill_embedding

        indices = similarities.argsort()[::-1]
        top_indices = []
        uris = set()
        idx = 0

        while len(top_indices) < top_k and idx < len(indices):
            uri = self.embedding_index.skills[indices[idx]].uri
            if uri not in uris:
                top_indices.append(indices[idx])
                uris.add(uri)

            idx += 1

        return [(self.embedding_index.skills[i], similarities[i]) for i in top_indices]