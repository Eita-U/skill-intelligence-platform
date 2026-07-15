from src.normalization.embedding_index import EmbeddingIndex
from src.normalization.embedding_linker import EmbeddingLinker
from src.normalization.embedding_model import EmbeddingModel
from src.normalization.reranker import MiniLMReranker, BGEReranker


def main():
    model = EmbeddingModel(model_name="BAAI/bge-m3", batch_size=64)
    index = EmbeddingIndex(embedding_model=model)
    index.load("data/embeddings/esco_bge-m3.npz")

    linker = EmbeddingLinker(index)

    results = linker.link_skills("ML and AI", top_k=20)

    for skill, score in results:
        print(f"{score:.3f} | {skill.preferred_label}")

    skill_candidates = [skill for skill, score in results]
    reranker = BGEReranker()
    reranked_results = reranker.rerank("python programming", skill_candidates, include_description=True)

    for skill, score in reranked_results:
        print(f"{score:.3f} | {skill.preferred_label}")
if __name__ == "__main__":
    main()