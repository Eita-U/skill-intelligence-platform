from src.data.esco_loader import load_esco_skills
from src.normalization.embedding_index import EmbeddingIndex
from src.normalization.embedding_model import EmbeddingModel


def main():
    skills = load_esco_skills("data/raw/esco/skills_en.csv")
    model = EmbeddingModel(model_name="BAAI/bge-m3", batch_size=64)
    index = EmbeddingIndex(embedding_model=model)
    index.build(skills, include_description=False)
    index.save("data/embeddings/esco_bge-m3.npz")


if __name__ == "__main__":
    main()