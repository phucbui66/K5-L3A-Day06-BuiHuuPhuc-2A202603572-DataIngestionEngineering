
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DB_PATH = ROOT / "data" / "vector_store"
PROCESSED = ROOT / "data" / "processed"
BATCH_SIZE = 32

STRATEGIES = {
    "fixed": "chunks_fixed.jsonl",
    "paragraph": "chunks_paragraph.jsonl",
}


def load_chunks(path):
    if not path.exists():
        raise FileNotFoundError(path)

    with path.open("r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    if not records:
        raise ValueError(f"No chunks in {path}")

    return records


def prepare_metadata(record):
    metadata = {
        "document_id": record["document_id"],
        "source": record["source"],
        "page": int(record["page"]),
    }

    for key, value in record.get("metadata", {}).items():
        if isinstance(value, (str, int, float, bool)):
            metadata[key] = value

    return metadata


def main():
    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    dimension = model.get_sentence_embedding_dimension()
    print("Model:", MODEL_NAME)
    print("Dimensions:", dimension)

    client = chromadb.PersistentClient(path=str(DB_PATH))

    for strategy, filename in STRATEGIES.items():
        start_time = time.perf_counter()
        records = load_chunks(PROCESSED / filename)

        collection_name = f"python_docs_{strategy}"

        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

        # Prevent mixing collections with different distance metrics.
        if collection.metadata.get("hnsw:space") != "cosine":
            raise RuntimeError(
                f"Collection {collection_name} is not configured for cosine"
            )

        print(f"\nBuilding {collection_name}...")

        for start in range(0, len(records), BATCH_SIZE):
            batch = records[start:start + BATCH_SIZE]

            texts = [r["text"] for r in batch]

            embeddings = model.encode(
                texts,
                normalize_embeddings=True,
                show_progress_bar=False,
            )

            collection.upsert(
                ids=[r["chunk_id"] for r in batch],
                embeddings=embeddings.tolist(),
                documents=texts,
                metadatas=[prepare_metadata(r) for r in batch],
            )

            print(
                f"\rProcessed {min(start + BATCH_SIZE, len(records))}"
                f"/{len(records)}",
                end="",
                flush=True,
            )

        print()

        expected_ids = {r["chunk_id"] for r in records}
        stored_ids = set(collection.get(include=[])["ids"])

        if stored_ids != expected_ids:
            raise RuntimeError(
                f"Collection mismatch: expected {len(expected_ids)}, "
                f"stored {len(stored_ids)}"
            )

        elapsed = time.perf_counter() - start_time

        print("Collection:", collection_name)
        print("Stored chunks:", collection.count())
        print("Time (seconds):", round(elapsed, 2))
        print("PASS: Persistent vector store verified")

    print("\nALL COLLECTIONS BUILT SUCCESSFULLY")


if __name__ == "__main__":
    main()
