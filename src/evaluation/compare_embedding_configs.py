from src.data.resume_ner import load_resume_skill_entities
from src.normalization.embedding_linker import EmbeddingLinker
from src.normalization.embedding_model import EmbeddingModel

CONFIGS = [
    {
        "name": "minilm_label_only",
        "model_name": "sentence-transformers/all-MiniLM-L6-v2",
        "include_description": False,
    },
    {
        "name": "minilm_with_description",
        "model_name": "sentence-transformers/all-MiniLM-L6-v2",
        "include_description": True,
    },
    {
        "name": "bge_m3_label_only",
        "model_name": "BAAI/bge-m3",
        "include_description": False,
    },
    {
        "name": "bge_m3_with_description",
        "model_name": "BAAI/bge-m3",
        "include_description": True,
    },
]

for config in CONFIGS:
    resumes = load_resume_skill_entities("data/raw/resume_ner/Entity Recognition in Resumes.json")
    model = EmbeddingModel(model_name=config["model_name"], batch_size=64)
    linker = EmbeddingLinker(embedding_model=model, include_description=config["include_description"])
    