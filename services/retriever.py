from sentence_transformers import SentenceTransformer
import faiss

from services.catalog_loader import load_catalog


class SHLRetriever:
    _model = None
    _catalog = None
    _documents = None
    _embeddings = None
    _index = None

    def __init__(self):

        if SHLRetriever._catalog is None:
            print("Loading SHL Catalog...")
            SHLRetriever._catalog = load_catalog()

        self.catalog = SHLRetriever._catalog

        if SHLRetriever._model is None:
            print("Loading Embedding Model...")
            SHLRetriever._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

        self.model = SHLRetriever._model

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

        if SHLRetriever._embeddings is None:

            print("Generating Embeddings...")

            SHLRetriever._embeddings = self.model.encode(
                self.documents,
                convert_to_numpy=True,
                show_progress_bar=True
            )

            faiss.normalize_L2(SHLRetriever._embeddings)

        self.embeddings = SHLRetriever._embeddings

        if SHLRetriever._index is None:

            print("Creating FAISS Index...")

            dimension = self.embeddings.shape[1]

            index = faiss.IndexFlatIP(dimension)

            index.add(self.embeddings)

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