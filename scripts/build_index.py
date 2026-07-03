from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from services.catalog_loader import load_catalog

print("Loading catalog...")
catalog = load_catalog()

documents = []

for assessment in catalog:
    documents.append(f"""
Assessment Name: {assessment.get("name","")}

Description:
{assessment.get("description","")}

Job Levels:
{", ".join(assessment.get("job_levels", []))}

Skills:
{", ".join(assessment.get("keys", []))}

URL:
{assessment.get("link","")}
""".strip())

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embeddings...")
embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    show_progress_bar=True
)

faiss.normalize_L2(embeddings)

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

Path("indexes").mkdir(exist_ok=True)

print("Saving embeddings...")
np.save("indexes/embeddings.npy", embeddings)

print("Saving FAISS index...")
faiss.write_index(index, "indexes/faiss.index")

print("Done!")