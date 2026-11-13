
import json
import time
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]

BENCHMARK_DIR = ROOT / "data" / "benchmark"
DB_DIR = ROOT / "data" / "vector_store"
OUTPUT_DIR = ROOT / "data" / "results"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

STRATEGIES = {
    "A": "python_docs_fixed",
    "B": "python_docs_paragraph",
    "C": "python_docs_paragraph",
}


def load_questions():
    questions = []

    for split in ("dev", "test"):
        path = BENCHMARK_DIR / f"{split}.json"

        with path.open(encoding="utf-8") as f:
            records = json.load(f)

        for record in records:
            questions.append({
                **record,
                "split": split,
            })

    return questions


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    questions = load_questions()

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(path=str(DB_DIR))

    collections = {
        name: client.get_collection(name)
        for name in set(STRATEGIES.values())
    }

    print("Questions:", len(questions))
    print("Running retrieval A/B/C...")

    # Encode each question once, reuse across all strategies.
    embeddings = model.encode(
        [q["question"] for q in questions],
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    results = []

    for strategy, collection_name in STRATEGIES.items():
        collection = collections[collection_name]
        start_time = time.perf_counter()

        for q, embedding in zip(questions, embeddings):
            # Strategy C applies a filter only when specified
            where = (
                q.get("filter")
                if strategy == "C"
                else None
            )

            query_args = {
                "query_embeddings": [embedding.tolist()],
                "n_results": 3,
                "include": [
                    "documents",
                    "metadatas",
                    "distances",
                ],
            }

            if where:
                query_args["where"] = where

            response = collection.query(**query_args)

            top3 = []

            for rank, (
                chunk_id,
                document,
                metadata,
                distance,
            ) in enumerate(
                zip(
                    response["ids"][0],
                    response["documents"][0],
                    response["metadatas"][0],
                    response["distances"][0],
                ),
                start=1,
            ):
                top3.append({
                    "rank": rank,
                    "chunk_id": chunk_id,
                    "document_id": metadata.get(
                        "document_id",
                        chunk_id.split("_p")[0],
                    ),
                    "source": metadata.get("source"),
                    "page": metadata.get("page"),
                    "section": metadata.get("section"),
                    "unit_id": metadata.get("unit_id"),
                    "distance": float(distance),
                    "text": document,
                })

            results.append({
                "question_id": q["question_id"],
                "split": q["split"],
                "strategy": strategy,
                "question": q["question"],
                "answer": q["answer"],
                "gold_sources": q["gold_sources"],
                "gold_evidence": q["gold_evidence"],
                "filter": q.get("filter"),
                "top3": top3,
            })

        elapsed = time.perf_counter() - start_time

        print(
            f"{strategy}: {len(questions)} questions "
            f"| {elapsed:.2f}s"
        )

    output = OUTPUT_DIR / "retrieval_top3.jsonl"

    with output.open("w", encoding="utf-8") as f:
        for record in results:
            f.write(
                json.dumps(record, ensure_ascii=False)
                + "\n"
            )

    assert len(results) == len(questions) * 3

    print("Total retrieval records:", len(results))
    print("Output:", output)
    print("PASS: Retrieval A/B/C completed")


if __name__ == "__main__":
    main()
