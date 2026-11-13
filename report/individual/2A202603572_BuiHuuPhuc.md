# Báo cáo cá nhân — Day 6


## Dữ liệu và pipeline

### 1. Chủ đề, nguồn/quyền, số trang và quy tắc tính trang

Tôi sử dụng bộ tài liệu Python Tutorial phiên bản 3.15 để xây dựng hệ thống tìm kiếm thông tin bằng semantic search.

Dữ liệu gồm 17 file TXT, chia theo các chủ đề như `controlflow`, `classes`, `datastructures`, `errors`, `modules`, `stdlib` và `stdlib2`.

Thông tin nguồn được lưu trong `starter/data/manifest.json`, bao gồm tên tài liệu, đường dẫn, giấy phép, phiên bản và vị trí nội dung.

- Nguồn: Python Tutorial.
- Phiên bản: Python 3.15.
- Giấy phép được ghi trong manifest: `PSF-2.0`.
- Số file TXT: 17.
- Tổng nội dung sau chuẩn hóa: khoảng 259.585 ký tự.
- Số đơn vị nguồn hợp lệ: 90.
- Độ dài tối thiểu mỗi đơn vị: 1.500 ký tự.

Do dữ liệu là TXT, không có số trang vật lý như PDF, tôi chia nội dung thành các đơn vị nguồn theo thứ tự xuất hiện. Mỗi đơn vị có `unit_id`, vị trí bắt đầu, vị trí kết thúc và số ký tự.

Cách này giúp đáp ứng yêu cầu tối thiểu 30 đơn vị nguồn có nội dung hợp lệ và vẫn có thể truy vết về tài liệu ban đầu.

### 2. Chuẩn hóa, lỗi và giới hạn

Pipeline được xây dựng bằng Python, gồm các bước:

1. Đọc tài liệu TXT từ `starter/data/raw/tutorial/`.
2. Chuẩn hóa văn bản.
3. Chia tài liệu thành các đơn vị nguồn.
4. Chia nội dung thành chunk theo từng chiến lược.
5. Tạo embedding cho các chunk.
6. Lưu vector vào ChromaDB.
7. Truy xuất Top-3 và đánh giá kết quả.

Các hàm xử lý chính được triển khai trong:

- `starter/src/ingestion.py`
- `starter/src/chunking.py`
- `starter/src/models.py`

Mỗi chunk được giữ thông tin nguồn và offset để có thể xác định vị trí trong tài liệu gốc.

Các giới hạn hiện tại:

- Chỉ xử lý dữ liệu TXT trong thí nghiệm chính.
- Chưa hoàn thiện chức năng đọc PDF.
- Chunk cố định có thể cắt ngang câu hoặc đoạn giải thích.
- Chunk theo đoạn văn có thể tách ví dụ khỏi phần giải thích nếu nội dung quá dài.
- Dữ liệu chủ yếu bằng tiếng Anh, trong khi câu hỏi benchmark bằng tiếng Việt.

### 3. Embedding model, vector store, metric, lệnh chạy và chi phí

| Thành phần | Cấu hình |
|---|---|
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| Provider | Local |
| Sentence Transformers | `6.3.0` |
| Số chiều embedding | 384 |
| Vector store | ChromaDB |
| ChromaDB version | `1.5.9` |
| Similarity metric | Cosine |
| Collection A | `python_docs_fixed` |
| Collection B/C | `python_docs_paragraph` |
| Đường dẫn lưu vector | `starter/data/vector_store/` |
| Chi phí API | 0 đồng |

Tôi sử dụng cùng embedding model và metric cho cả ba chiến lược để bảo đảm việc so sánh không bị ảnh hưởng bởi thay đổi mô hình.

Embedding được chuẩn hóa trước khi lưu vào ChromaDB. Dữ liệu vector được lưu bền vững và có thể sử dụng lại.

Các lệnh chạy chính từ thư mục `starter`:

```powershell
python scripts/build_chunks.py
python scripts/build_vector_store.py
python scripts/validate_benchmark.py
python scripts/run_retrieval.py
python scripts/evaluate_retrieval.py
python scripts/analyze_ingestion.py
```

Chi phí API bằng 0 đồng vì embedding chạy trên máy cá nhân. Chi phí điện và tài nguyên máy tính chưa được quy đổi thành tiền.

### 4. Metadata bắt buộc, trường lọc bổ sung, nguồn giá trị và lý do chọn

Các trường metadata được sử dụng:

| Metadata | Ý nghĩa |
|---|---|
| `document_id` | ID của tài liệu gốc |
| `source` | Tên file nguồn |
| `page` | Số thứ tự đơn vị nguồn trong tài liệu |
| `unit_id` | ID đơn vị nguồn |
| `section` | Chủ đề của tài liệu |
| `version` | Phiên bản tài liệu |
| `start_offset` | Vị trí bắt đầu |
| `end_offset` | Vị trí kết thúc |
| `chunk_index` | Số thứ tự chunk |
| `strategy` | Chiến lược chia chunk |
| `char_count` | Số ký tự của chunk |

Trong đó:

- `document_id`, `source` và `page` dùng để truy vết nguồn.
- `section` dùng để lọc kết quả theo chủ đề.
- `start_offset` và `end_offset` giúp xác định vị trí nội dung.
- `strategy` giúp phân biệt kết quả giữa các cách chia chunk.

Tôi chọn `section` làm trường lọc chính vì dữ liệu Python Tutorial được tổ chức theo các chủ đề rõ ràng.

## Cấu hình và benchmark

### 1. Cấu hình A / B / C

| Thành phần | Strategy A | Strategy B | Strategy C |
|---|---|---|---|
| Chunking | Fixed-size | Paragraph-aware | Paragraph-aware |
| Chunk size | 500 ký tự | Tối đa 500 ký tự | Tối đa 500 ký tự |
| Overlap | 50 ký tự | Không overlap cố định | Không overlap cố định |
| Embedding | `all-MiniLM-L6-v2` | `all-MiniLM-L6-v2` | `all-MiniLM-L6-v2` |
| Vector store | ChromaDB | ChromaDB | ChromaDB |
| Metric | Cosine | Cosine | Cosine |
| Metadata filter | Không | Không | Có, khi câu hỏi yêu cầu |
| Số chunk | 614 | 708 | 708 |

**Strategy A — Fixed-size chunking**

Chia tài liệu thành các chunk có kích thước 500 ký tự và overlap 50 ký tự.

Ưu điểm là dễ triển khai, kích thước chunk ổn định. Nhược điểm là có thể cắt ngang câu hoặc đoạn văn.

**Strategy B — Paragraph-aware chunking**

Chia nội dung dựa trên ranh giới đoạn văn, giới hạn tối đa 500 ký tự.

Mục tiêu là giữ nội dung trong chunk mạch lạc hơn so với chia cố định.

**Strategy C — Paragraph-aware + metadata filter**

Sử dụng cùng cách chia chunk, embedding và vector store như B.

Điểm khác biệt duy nhất khi truy xuất là áp dụng metadata filter nếu câu hỏi có điều kiện lọc.

Ví dụ:

```python
where = {"section": "stdlib2"}
```

So sánh A–B giúp đánh giá tác động của chunking. So sánh B–C giúp đánh giá tác động của metadata filter.

### 2. Benchmark và cách kiểm chứng evidence

Bộ benchmark gồm 20 câu hỏi:

| Tập dữ liệu | Số câu |
|---|---:|
| Dev | 15 |
| Test | 5 |
| Tổng | 20 |

Mỗi câu hỏi có:

- `question_id`
- `question`
- `expected_answer`
- `gold_source`
- `gold_page`
- `gold_evidence`
- `required_filter` nếu có

Các câu hỏi kiểm tra metadata filter gồm:

| Question ID | Required filter |
|---|---|
| `D02` | `section=controlflow` |
| `D07` | `section=classes` |
| `D15` | `section=venv` |
| `T05` | `section=stdlib2` |

Trong đó `T05` thuộc tập test.

Bộ benchmark được lưu tại:

- `starter/data/benchmark/dev.json`
- `starter/data/benchmark/test.json`

Tôi sử dụng `scripts/validate_benchmark.py` để kiểm tra cấu trúc câu hỏi và đoạn evidence trong dữ liệu nguồn.

Cùng một bộ benchmark được sử dụng cho cả ba chiến lược.

### 3. Tiêu chí chọn chiến lược

Tiêu chí lựa chọn là ưu tiên khả năng tìm đúng bằng chứng trong Top-3 trên tập dev.

Sau đó xem xét:

1. Tính mạch lạc của chunk.
2. Khả năng truy vết nguồn.
3. Khả năng lọc metadata.
4. Số lượng chunk và tài nguyên sử dụng.

Nếu các chiến lược có kết quả truy xuất tương đương, tôi ưu tiên chiến lược có chunk dễ hiểu và hỗ trợ metadata filter.

Chưa có bằng chứng độc lập xác nhận thời điểm tiêu chí này được ghi nhận trước khi xem kết quả test.

## Kết quả

### 1. Retrieval Accuracy

Kết quả tự động đã ghi nhận:

| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Chunk count | Thời gian | Chi phí |
|---|---|---|---|---|---|---|
| A | Dev | 3/15 | 5/15 | 614 | 0,12 giây | 0đ |
| A | Test | 2/5 | 2/5 | 614 | 0,12 giây | 0đ |
| B | Dev | 5/15 | 6/15 | 708 | 0,10 giây | 0đ |
| B | Test | 1/5 | 1/5 | 708 | 0,10 giây | 0đ |
| C | Dev | 5/15 | 6/15 | 708 | 0,03 giây | 0đ |
| C | Test | 1/5 | 2/5 | 708 | 0,03 giây | 0đ |

**Lưu ý về cách tính:**

- `Hit@1` hiện là kết quả tự động dựa trên đơn vị nguồn gold.
- `Evidence Hit@3` là chỉ số gần đúng, sử dụng đối sánh văn bản.
- Hai chỉ số chưa được xác nhận hoàn toàn theo yêu cầu chunk phải thuộc nguồn/trang gold và chứa đủ bằng chứng.
- Thời gian là thời gian truy xuất ghi nhận theo chiến lược, không phải thời gian riêng cho từng split.

Vì vậy, bảng trên phản ánh kết quả đánh giá tự động hiện có, chưa phải kết quả kiểm chứng thủ công cuối cùng.

### 2. Thống kê ingestion

| Chỉ số | Strategy A | Strategy B | Strategy C |
|---|---:|---:|---:|
| Chunk count | 614 | 708 | 708 |
| Độ dài trung bình | 465,45 | 366,65 | 366,65 |
| Median | 500 | 401,5 | 401,5 |
| P95 | 500 | 492 | 492 |
| Chunk dài nhất | 500 | 500 | 500 |
| Thời gian ingest | 14,07 giây | 15,59 giây | 15,59 giây |

Strategy B và C tạo nhiều chunk hơn A vì chia nội dung theo đoạn văn.

Quá trình kiểm tra idempotence cho thấy khi chạy lại thao tác upsert, số lượng vector vẫn giữ nguyên, không tạo thêm bản ghi trùng lặp.

### 3. Chunk Coherence, Metadata và Grounding

| Strategy | Coherence trung bình /2 (n) | Metadata đủ và nhất quán với ID (n/N) | Filter tuân thủ | Grounding 0/1/2 (số câu) và trung bình /2 |
|---|---|---|---|---|
| A | 0,40 (10) | 15/15 | 2/3 chunks | 0: 1, 1: 1, 2: 3 — TB 1,40 |
| B | 1,50 (10) | 15/15 | 1/3 chunks | 0: 3, 1: 1, 2: 1 — TB 0,60 |
| C | 1,50 (10) | 15/15 | 3/3 chunks | 0: 2, 1: 1, 2: 2 — TB 1,00 |

#### Chunk Coherence

Tôi sử dụng cùng 10 vị trí nguồn để đánh giá cả ba chiến lược.

Thang điểm:

- `0`: Chunk bị cắt ngang ý, thiếu ngữ cảnh.
- `1`: Hiểu được một phần nhưng chưa đầy đủ.
- `2`: Nội dung rõ ràng, giữ được ý chính.

Kết quả:

| Strategy | Tổng điểm | Trung bình /2 | Tỷ lệ điểm tối đa |
|---|---:|---:|---:|
| A | 4/20 | 0,40 | 20% |
| B | 15/20 | 1,50 | 75% |
| C | 15/20 | 1,50 | 75% |

B và C có kết quả giống nhau vì sử dụng cùng cách chia chunk.

Kết quả cho thấy chia theo đoạn văn giữ nội dung mạch lạc hơn so với chia cố định trong mẫu đánh giá này.

#### Metadata Usefulness

Tôi kiểm tra 45 kết quả truy xuất, tương ứng:

`5 câu test × 3 chiến lược × Top-3 = 45 bản ghi`

Các trường `source`, `page`, `section` đều có mặt và nhất quán với cách đặt ID chunk.

Với câu `T05`, yêu cầu lọc:

```python
{"section": "stdlib2"}
```

Kết quả:

| Strategy | Số chunk thuộc `stdlib2` | Tỷ lệ |
|---|---:|---:|
| A | 2/3 | 66,67% |
| B | 1/3 | 33,33% |
| C | 3/3 | 100% |

C tuân thủ filter tốt nhất vì sử dụng điều kiện lọc trực tiếp trong truy xuất.

Tuy nhiên, việc có đúng metadata không đồng nghĩa với việc chunk chứa đủ bằng chứng trả lời.

Ngoài ra, kết quả metadata hiện mới xác nhận sự đầy đủ của trường và tính nhất quán với ID. Chưa kiểm chứng độc lập toàn bộ 45 bản ghi với văn bản nguồn.

#### Grounding Quality

Grounding được đánh giá trên 5 câu test cho mỗi chiến lược.

Thang điểm:

- `0`: Không có bằng chứng trả lời.
- `1`: Có bằng chứng liên quan nhưng chưa đủ.
- `2`: Có đủ bằng chứng và truy vết được nguồn.

Kết quả chi tiết:

| Question ID | Strategy A | Strategy B | Strategy C |
|---|---:|---:|---:|
| `T01` | 2 | 0