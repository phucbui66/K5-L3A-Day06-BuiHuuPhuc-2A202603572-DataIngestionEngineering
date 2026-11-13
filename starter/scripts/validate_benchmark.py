
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "data" / "benchmark"
SOURCE_UNITS = ROOT / "data" / "processed" / "source_units.jsonl"


def main():
    with SOURCE_UNITS.open(encoding="utf-8") as f:
        units = {
            unit["unit_id"]: unit
            for line in f
            if line.strip()
            for unit in [json.loads(line)]
        }

    all_questions = []
    seen_ids = set()

    for split, expected in [("dev", 15), ("test", 5)]:
        path = BENCHMARK / f"{split}.json"

        with path.open(encoding="utf-8") as f:
            questions = json.load(f)

        assert len(questions) == expected

        for q in questions:
            qid = q["question_id"]

            assert qid not in seen_ids, f"Duplicate: {qid}"
            seen_ids.add(qid)

            assert q["question"].strip()
            assert q["answer"].strip()
            assert q["gold_evidence"].strip()
            assert q["gold_sources"]

            for gold in q["gold_sources"]:
                unit = units[gold["unit_id"]]

                assert gold["document_id"] == unit["document_id"]
                assert gold["source"] == unit["source"]
                assert gold["page"] == unit["page"]

                assert q["gold_evidence"] in unit["text"], (
                    f"Evidence mismatch: {qid}"
                )

                if q.get("filter"):
                    assert unit["section"] == q["filter"]["section"]

            all_questions.append(q)

        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"{split}: {len(questions)} questions")
        print(f"{split} SHA256: {digest}")

    assert len(all_questions) == 20
    assert sum(bool(q.get("filter")) for q in all_questions) >= 3
    assert any(q.get("filter") for q in all_questions[15:])

    print("PASS: 20 questions, source references and evidence verified")


if __name__ == "__main__":
    main()
