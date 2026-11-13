# Grounding & Metadata Audit – Day 06

## Grounding (manual review, 5 test questions × 3 strategies)

| Question | A | B | C |
|---|---:|---:|---:|
| T01 | 2 | 0 | 0 |
| T02 | 1 | 1 | 1 |
| T03 | 2 | 2 | 2 |
| T04 | 2 | 0 | 0 |
| T05 | 0 | 0 | 2 |
| **Average /2** | **1.40** | **0.60** | **1.00** |

Score 0: no usable evidence; 1: partial evidence; 2: sufficient evidence with source. This assesses retrieval evidence, not LLM answer correctness.

## Metadata audit (45 Top-3 records)

| Strategy | Fields present and consistent with chunk ID | Filter compliance on T05 |
|---|---:|---:|
| A | 15/15 | 2/3 |
| B | 15/15 | 1/3 |
| C | 15/15 | 3/3 |

**Scope:** This audit checks `source`, `page`, and `section` against the chunk ID and the source naming convention in the supplied review. It does **not** independently compare all 45 records with the original normalized source text; do not label it a full source-level verification.

## Grounding reasons

### T01
- A (2/2): Rank 3 nêu biểu diễn nhị phân của 1/10 chỉ xấp xỉ; đủ trả lời.
- B (0/2): Top-3 không giải thích vì sao phân số thập phân không biểu diễn chính xác.
- C (0/2): Top-3 không giải thích vì sao phân số thập phân không biểu diễn chính xác.

### T02
- A (1/2): Có ví dụ pop() hoặc del, nhưng thiếu so sánh trực tiếp del theo chỉ số và giá trị trả về của pop().
- B (1/2): Có ví dụ pop() hoặc del, nhưng thiếu so sánh trực tiếp del theo chỉ số và giá trị trả về của pop().
- C (1/2): Có ví dụ pop() hoặc del, nhưng thiếu so sánh trực tiếp del theo chỉ số và giá trị trả về của pop().

### T03
- A (2/2): Rank 1 nói rõ datetime hỗ trợ đối tượng timezone-aware.
- B (2/2): Rank 1 nói rõ datetime hỗ trợ đối tượng timezone-aware.
- C (2/2): Rank 1 nói rõ datetime hỗ trợ đối tượng timezone-aware.

### T04
- A (2/2): Rank 1 ghi rõ F3 vào paste mode và nhấn lại để về prompt.
- B (0/2): Top-3 không có hướng dẫn F3.
- C (0/2): Top-3 không có hướng dẫn F3.

### T05
- A (0/2): Top-3 không chứa giải thích về responsiveness khi chạy tác vụ nền.
- B (0/2): Top-3 không chứa giải thích về responsiveness khi chạy tác vụ nền.
- C (2/2): Rank 3 mô tả rõ threading chạy tác vụ nền và ứng dụng tiếp tục nhận input.
