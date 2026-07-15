from pathlib import Path

import numpy as np


from src.models.skill import Skill
from src.normalization.text_builder import build_skill_text
from src.normalization.embedding_model import EmbeddingModel

class EmbeddingIndex:
    def __init__(self, embedding_model: EmbeddingModel = None):
        self.embedding_model = embedding_model or EmbeddingModel()
        self.skills: list[Skill] = []
        self.texts: list[str] = []
        self.embeddings = None

    def build(self, skills: list[Skill], include_description: bool = False) -> None:
        self.skills = skills
        self.texts = [build_skill_text(skill, include_description) for skill in skills]
        self.embeddings = self.embedding_model.encode(self.texts)

    def save(self, path: str | Path) -> None:
        if self.embeddings is None:
            raise ValueError("Embedding index has not been built.")

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        np.savez_compressed(
            path,
            embeddings=self.embeddings,
            texts=np.array(self.texts),
            uris=np.array([skill.uri for skill in self.skills]),
            labels=np.array([skill.preferred_label for skill in self.skills]),
            skill_types=np.array([skill.skill_type for skill in self.skills]),
            descriptions=np.array([skill.description for skill in self.skills]),
        )
    
    def load(self, path: str | Path) -> None:
        data = np.load(path, allow_pickle=False)

        self.embeddings = data["embeddings"]
        self.texts = data["texts"].tolist()
        self.skills = [
            Skill(
                uri=uri,
                preferred_label=label,
                skill_type=skill_type,
                description=description,
            )
            for uri, label, skill_type, description in zip(
                data["uris"],
                data["labels"],
                data["skill_types"],
                data["descriptions"],
            )
        ]