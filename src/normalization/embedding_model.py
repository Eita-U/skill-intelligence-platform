from sentence_transformers import SentenceTransformer
import numpy as np
import torch


class EmbeddingModel:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        batch_size: int = 64,
        device: str = "cpu"
    ):
        self.batch_size = batch_size
        self.device = "cuda" if device == "cuda" and torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        self.model = SentenceTransformer(model_name, device=self.device)

    def encode(self, texts: list[str]) -> np.ndarray:
        return self.model.encode(texts, batch_size=self.batch_size, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)