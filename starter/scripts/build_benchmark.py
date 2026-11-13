
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "processed" / "source_units.jsonl"
OUTPUT = ROOT / "data" / "benchmark"

# ID, question, answer, source unit, evidence anchor, filter section
QUESTIONS = [
    (
        "D01",
        "Trong Python, nhánh elif và else của if có bắt buộc không?",
        "Có thể có 0 hoặc nhiều elif; else là tùy chọn.",
        "python_controlflow_unit_001",
        'There can be zero or more "elif" parts',
        None,
    ),
    (
        "D02",
        "Tại sao range() tiết kiệm bộ nhớ hơn danh sách tạo sẵn?",
        "range() tạo đối tượng iterable cung cấp lần lượt các phần tử khi lặp, không tạo toàn bộ danh sách.",
        "python_controlflow_unit_002",
        'In many ways the object returned by "range()"',
        "controlflow",
    ),
    (
        "D03",
        "Lệnh break và continue khác nhau thế nào?",
        "break thoát vòng lặp bao quanh gần nhất; continue chuyển sang lượt lặp kế tiếp.",
        "python_controlflow_unit_002",
        'The "break" statement breaks out of the innermost',
        None,
    ),
    (
        "D04",
        "Khi nào else của vòng lặp for được thực thi?",
        "Khi vòng lặp kết thúc mà không gặp break.",
        "python_controlflow_unit_003",
        'When used with a loop, the "else" clause',
        None,
    ),
    (
        "D05",
        "Trong match-case, ký hiệu _ có ý nghĩa gì?",
        "_ là wildcard, luôn khớp khi được xét.",
        "python_controlflow_unit_004",
        'Note the last block: the "variable name" "_"',
        None,
    ),
    (
        "D06",
        "Phương thức __init__ được gọi khi nào?",
        "Được tự động gọi khi tạo instance nếu lớp định nghĩa __init__.",
        "python_classes_unit_005",
        'When a class defines an "__init__()" method',
        None,
    ),
    (
        "D07",
        "Vì sao không nên dùng list mutable làm class variable cho dữ liệu riêng từng đối tượng?",
        "Vì danh sách đó được chia sẻ giữa các instance; nên dùng instance variable.",
        "python_classes_unit_007",
        "As discussed in A Word About Names and Objects",
        "classes",
    ),
    (
        "D08",
        "Tên self có phải từ khóa đặc biệt của Python không?",
        "Không; self chỉ là quy ước đặt tên tham số đầu tiên của method.",
        "python_classes_unit_008",
        'Often, the first argument of a method is called "self"',
        None,
    ),
    (
        "D09",
        "Điều gì báo hiệu iterator đã hết phần tử?",
        "__next__() phát sinh StopIteration, báo cho for dừng lại.",
        "python_classes_unit_012",
        'raises a "StopIteration" exception',
        None,
    ),
    (
        "D10",
        "Python phân biệt hai loại lỗi cơ bản nào trong phần Errors and Exceptions?",
        "Syntax errors và exceptions.",
        "python_errors_unit_001",
        "syntax errors* and",
        None,
    ),
    (
        "D11",
        "Lệnh raise dùng để làm gì?",
        "Chủ động phát sinh một exception được chỉ định.",
        "python_errors_unit_004",
        'The "raise" statement allows the programmer',
        None,
    ),
    (
        "D12",
        "Vì sao phải mở file ảnh JPEG ở binary mode?",
        "Text mode tự chuyển đổi ký tự xuống dòng theo nền tảng, có thể làm hỏng dữ liệu nhị phân.",
        "python_inputoutput_unit_005",
        "In text mode, the default when reading",
        None,
    ),
    (
        "D13",
        "Serialization và deserialization trong JSON là gì?",
        "Serialization chuyển dữ liệu thành biểu diễn chuỗi; deserialization khôi phục dữ liệu từ chuỗi.",
        "python_inputoutput_unit_007",
        "this process is called",
        None,
    ),
    (
        "D14",
        "Tại sao mã xử lý dòng lệnh trong module có thể không chạy khi import?",
        "Vì mã được đặt trong nhánh chỉ chạy khi module là file main.",
        "python_modules_unit_003",
        "you can make the file usable as a script",
        None,
    ),
    (
        "D15",
        "Kích hoạt virtual environment ảnh hưởng đến lệnh python như thế nào?",
        "Nó thay đổi môi trường và prompt để lệnh python dùng bản cài Python của virtual environment đó.",
        "python_venv_unit_002",
        "Activating the virtual environment will change",
        "venv",
    ),
    (
        "T01",
        "Vì sao nhiều số thập phân không thể biểu diễn chính xác bằng float nhị phân?",
        "Vì phần lớn phân số thập phân không thể biểu diễn chính xác bằng phân số nhị phân hữu hạn.",
        "python_floatingpoint_unit_001",
        "most decimal fractions cannot be represented exactly",
        None,
    ),
    (
        "T02",
        "Khác biệt giữa del theo chỉ số và pop() của list là gì?",
        "del xóa phần tử theo chỉ số mà không trả về giá trị; pop() trả về giá trị đã xóa.",
        "python_datastructures_unit_005",
        "There is a way to remove an item from a list",
        None,
    ),
    (
        "T03",
        "Module datetime có hỗ trợ đối tượng nhận biết múi giờ không?",
        "Có, datetime hỗ trợ đối tượng timezone-aware.",
        "python_stdlib_unit_003",
        'The "datetime" module supplies classes',
        None,
    ),
    (
        "T04",
        "Trong interactive shell mới, phím F3 dùng để làm gì?",
        "F3 bật paste mode và nhấn lại để trở về prompt thường.",
        "python_appendix_unit_001",
        '"F3"\nenters "paste mode"',
        None,
    ),
    (
        "T05",
        "Theo tài liệu, threading giúp ứng dụng phản hồi người dùng tốt hơn như thế nào?",
        "Cho phép tác vụ chạy nền trong khi ứng dụng vẫn nhận đầu vào và tiếp tục công việc khác.",
        "python_stdlib2_unit_003",
        "Threading is a technique for decoupling tasks",
        "stdlib2",
    ),
]


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Missing {SOURCE}. Run export_source_units.py first."
        )

    units = {}
    with SOURCE.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                unit = json.loads(line)
                units[unit["unit_id"]] = unit

    OUTPUT.mkdir(parents=True, exist_ok=True)

    benchmark = []

    for qid, question, answer, unit_id, anchor, section in QUESTIONS:
        unit = units[unit_id]
        text = unit["text"]

        # Evidence must occur exactly once in the original source unit
        if text.count(anchor) != 1:
            raise ValueError(
                f"{qid}: evidence anchor not unique or not found"
            )

        start = text.index(anchor)
        evidence = text[start:start + 340].rstrip()

        assert evidence in text
        assert evidence.strip()

        if section is not None:
            assert unit["section"] == section

        benchmark.append({
            "question_id": qid,
            "question": question,
            "answer": answer,
            "gold_sources": [{
                "document_id": unit["document_id"],
                "source": unit["source"],
                "page": unit["page"],
                "unit_id": unit_id,
            }],
            "gold_evidence": evidence,
            "filter": (
                {"section": section}
                if section is not None
                else None
            ),
        })

    for split, records in [
        ("dev", benchmark[:15]),
        ("test", benchmark[15:]),
    ]:
        path = OUTPUT / f"{split}.json"

        path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )

        digest = hashlib.sha256(path.read_bytes()).hexdigest()

        print(f"{split}: {len(records)} questions")
        print(f"SHA256: {digest}")
        print(f"Saved: {path}")

    print("PASS: 20 benchmark questions generated")


if __name__ == "__main__":
    main()
