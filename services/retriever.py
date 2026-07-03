from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from services.catalog_loader import load_catalog


class SHLRetriever:
    _model = None
    _catalog = None
    _documents = None
    _embeddings = None
    _index = None

    INDEX_DIR = Path("indexes")
    EMBEDDINGS_FILE = INDEX_DIR / "embeddings.npy"
    FAISS_FILE = INDEX_DIR / "faiss.index"

    def __init__(self):

        # -------------------------
        # Load catalog
        # -------------------------
        if SHLRetriever._catalog is None:
            print("Loading SHL Catalog...")
            SHLRetriever._catalog = load_catalog()

        self.catalog = SHLRetriever._catalog

        # -------------------------
        # Load embedding model
        # -------------------------
        if SHLRetriever._model is None:
            print("Loading Embedding Model...")
            SHLRetriever._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

        self.model = SHLRetriever._model

        # -------------------------
        # Prepare documents
        # -------------------------
        if SHLRetriever._documents is None:

            documents = []

            for assessment in self.catalog:

                document = f"""
Assessment Name: {assessment.get("name", "")}

Description:
{assessment.get("description", "")}

Job Levels:
{", ".join(assessment.get("job_levels", []))}

Skills:
{", ".join(assessment.get("keys", []))}

URL:
{assessment.get("link", "")}
"""

                documents.append(document.strip())

            SHLRetriever._documents = documents

        self.documents = SHLRetriever._documents

        # -------------------------
        # Load embeddings
        # -------------------------
        if SHLRetriever._embeddings is None:

            if self.EMBEDDINGS_FILE.exists():

                print("Loading saved embeddings...")

                SHLRetriever._embeddings = np.load(
                    self.EMBEDDINGS_FILE
                )

            else:

                print("Generating embeddings...")

                SHLRetriever._embeddings = self.model.encode(
                    self.documents,
                    convert_to_numpy=True,
                    show_progress_bar=True
                )

                faiss.normalize_L2(
                    SHLRetriever._embeddings
                )

                self.INDEX_DIR.mkdir(exist_ok=True)

                np.save(
                    self.EMBEDDINGS_FILE,
                    SHLRetriever._embeddings
                )

        self.embeddings = SHLRetriever._embeddings

        # -------------------------
        # Load FAISS index
        # -------------------------
        if SHLRetriever._index is None:

            if self.FAISS_FILE.exists():

                print("Loading saved FAISS index...")

                SHLRetriever._index = faiss.read_index(
                    str(self.FAISS_FILE)
                )

            else:

                print("Creating FAISS index...")

                dimension = self.embeddings.shape[1]

                index = faiss.IndexFlatIP(
                    dimension
                )

                index.add(self.embeddings)

                faiss.write_index(
                    index,
                    str(self.FAISS_FILE)
                )

                SHLRetriever._index = index

        self.index = SHLRetriever._index

        print("Retriever Ready.")

    def search(self, query: str, top_k: int = 5):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(
            query_embedding,
            max(top_k * 2, 10)
        )

        results = []

        seen = set()

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            if score < 0.25:
                continue

            assessment = dict(self.catalog[idx])

            if assessment["name"] in seen:
                continue

            seen.add(assessment["name"])

            assessment["score"] = float(score)

            results.append(assessment)

            if len(results) >= top_k:
                break

        return results