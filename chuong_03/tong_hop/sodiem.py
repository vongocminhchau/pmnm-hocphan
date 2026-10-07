from flask import Flask, request, redirect, url_for, abort, make_response
from html import escape
import json


app = Flask(__name__)


# ============================================================
# PHẦN 0 - DỮ LIỆU MẪU
# ============================================================

STUDENTS = {
    "23T1020001": {
        "name": "Nguyễn Văn An",
        "lop": "K47A",
        "scores": {
            "PMMNM": 8.5,
            "CSDL": 7.0,
            "MMT": 9.0
        }
    },
    "23T1020002": {
        "name": "Trần Thị Bình",
        "lop": "K47A",
        "scores": {
            "PMMNM": 6.0,
            "CSDL": 5.5,
            "MMT": 7.0
        }
    },
    "23T1020003": {
        "name": "Lê Hoàng Cường",
        "lop": "K47B",
        "scores": {
            "PMMNM": 9.5,
            "CSDL": 9.0
        }
    },
    "23T1020004": {
        "name": "Phạm Minh Dũng",
        "lop": "K47B",
        "scores": {
            "PMMNM": 4.0,
            "CSDL": 3.5,
            "MMT": 5.0
        }
    },
    "23T1020005": {
        "name": "Hoàng Thu Hà",
        "lop": "K47A",
        "scores": {}
    },
    "23T1020006": {
        "name": "Võ Quốc Khánh",
        "lop": "K47C",
        "scores": {
            "PMMNM": 7.5,
            "MMT": 8.0
        }
    }
}


# ============================================================
# PHẦN 0 - HÀM PHỤ
# ============================================================

def average(scores):
    """
    Tính điểm trung bình.
    Dict rỗng -> None.
    Làm tròn 2 chữ số.
    """
    if not scores:
        return None

    return round(sum(scores.values()) / len(scores), 2)


def rank(avg):
    """
    Xếp loại theo điểm trung bình.
    """
    if avg is None:
        return "Chưa có điểm"

    if avg >= 8.5:
        return "Giỏi"

    if avg >= 7.0:
        return "Khá"

    if avg >= 5.0:
        return "Trung bình"

    return "Yếu"


def student_summary(mssv):
    """
    Trả về thông tin tổng hợp của một sinh viên.
    """
    student = STUDENTS[mssv]

    avg = average(student["scores"])

    return {
        "mssv": mssv,
        "name": student["name"],
        "lop": student["lop"],
        "scores": student["scores"],
        "average": avg,
        "rank": rank(avg)
    }


def layout(title, body):
    """
    Tạo khung HTML chung.
    Dùng escape() cho title và dữ liệu chèn vào HTML.
    """

    safe_title = escape(str(title))

    return f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>{safe_title} - Sổ điểm</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f5f5f5;
        }}

        nav {{
            background: #333;
            padding: 15px;
            margin-bottom: 25px;
        }}

        nav a {{
            color: white;
            text-decoration: none;
            margin-right: 20px;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            background: white;
        }}

        th, td {{
            border: 1px solid #ccc;
            padding: 10px;
            text-align: left;
        }}

        th {{
            background: #eee;
        }}

        a {{
            color: #0066cc;
        }}

        .box {{
            background: white;
            padding: 20px;
            border-radius: 8px;
        }}

        .error {{
            color: #b00020;
        }}

        input, button {{
            padding: 8px;
            margin: 5px;
        }}
    </style>
</head>

<body>

<nav>
    <a href="{url_for('home')}">Trang chủ</a>
    <a href="{url_for('student_list')}">Sinh viên</a>
    <a href="{url_for('search')}">Tìm kiếm</a>
</nav>

<div class="box">
    {body}
</div>

</body>
</html>
"""


# ============================================================
# PHẦN 1 - CÂU 1
# TRANG CHỦ
# ============================================================

@app.route("/")
def home():

    total_students = len(STUDENTS)

    total_classes = len(
        set(student["lop"] for student in STUDENTS.values())
    )

    body = f"""
        <h1>Sổ điểm lớp học</h1>

        <p>Tổng số sinh viên:
            <strong>{total_students}</strong>
        </p>

        <p>Số lớp:
            <strong>{total_classes}</strong>
        </p>

        <p>
            <a href="{url_for('student_list')}">
                Xem danh sách sinh viên
            </a>
        </p>

        <p>
            <a href="{url_for('api_students')}">
                API danh sách sinh viên
            </a>
        </p>
    """

    return layout("Trang chủ", body)


# ============================================================
# PHẦN 1 - CÂU 2
# DANH SÁCH SINH VIÊN
# ============================================================

@app.route("/students")
def student_list():

    lop_filter = request.args.get("lop", "")

    students = []

    for mssv, student in STUDENTS.items():

        if lop_filter:
            if student["lop"].lower() != lop_filter.lower():
                continue

        students.append(student_summary(mssv))

    classes = sorted(
        set(student["lop"] for student in STUDENTS.values())
    )

    filter_links = f"""
        <p>
            <strong>Lọc theo lớp:</strong>

            <a href="{url_for('student_list')}">
                Tất cả
            </a>
    """

    for lop in classes:
        filter_links += f"""
            |
            <a href="{url_for('student_list', lop=lop)}">
                {escape(lop)}
            </a>
        """

    filter_links += "</p>"

    if not students:

        table = """
            <p>Không có sinh viên phù hợp.</p>
        """

    else:

        rows = ""

        for student in students:

            avg = (
                "—"
                if student["average"] is None
                else escape(str(student["average"]))
            )

            rows += f"""
            <tr>
                <td>
                    <a href="{url_for(
                        'student_detail',
                        mssv=student['mssv']
                    )}">
                        {escape(student['mssv'])}
                    </a>
                </td>

                <td>{escape(student['name'])}</td>

                <td>
                    <a href="{url_for(
                        'student_list',
                        lop=student['lop']
                    )}">
                        {escape(student['lop'])}
                    </a>
                </td>

                <td>{avg}</td>

                <td>{escape(student['rank'])}</td>
            </tr>
            """

        table = f"""
        <table>

            <thead>
                <tr>
                    <th>MSSV</th>
                    <th>Họ tên</th>
                    <th>Lớp</th>
                    <th>Điểm TB</th>
                    <th>Xếp loại</th>
                </tr>
            </thead>

            <tbody>
                {rows}
            </tbody>

        </table>
        """

    body = f"""
        <h1>Danh sách sinh viên</h1>

        {filter_links}

        {table}
    """

    return layout("Sinh viên", body)


# ============================================================
# PHẦN 1 - CÂU 3
# CHI TIẾT SINH VIÊN
# ============================================================

@app.route("/students/<mssv>")
def student_detail(mssv):

    if mssv not in STUDENTS:

        abort(
            404,
            description=f"Không có sinh viên với MSSV = {mssv}."
        )

    student = student_summary(mssv)

    avg = (
        "—"
        if student["average"] is None
        else escape(str(student["average"]))
    )

    rows = ""

    if student["scores"]:

        for course, score in student["scores"].items():

            rows += f"""
            <tr>
                <td>{escape(course)}</td>
                <td>{escape(str(score))}</td>
            </tr>
            """

    else:

        rows = """
        <tr>
            <td colspan="2">
                Chưa có điểm
            </td>
        </tr>
        """

    body = f"""
        <h1>Chi tiết sinh viên</h1>

        <p>
            <strong>Họ tên:</strong>
            {escape(student['name'])}
        </p>

        <p>
            <strong>MSSV:</strong>
            {escape(student['mssv'])}
        </p>

        <p>
            <strong>Lớp:</strong>
            <a href="{url_for(
                'student_list',
                lop=student['lop']
            )}">
                {escape(student['lop'])}
            </a>
        </p>

        <p>
            <strong>Điểm trung bình:</strong>
            {avg}
        </p>

        <p>
            <strong>Xếp loại:</strong>
            {escape(student['rank'])}
        </p>

        <h2>Bảng điểm</h2>

        <table>
            <tr>
                <th>Học phần</th>
                <th>Điểm</th>
            </tr>

            {rows}
        </table>

        <br>

        <p>
            <a href="{url_for(
                'export_scores',
                mssv=mssv
            )}">
                Tải bảng điểm (CSV)
            </a>
        </p>

        <p>
            Link rút gọn:
            <a href="{url_for(
                'short_student',
                mssv=mssv
            )}">
                /sv/{escape(mssv)}
            </a>
        </p>
    """

    return layout("Chi tiết sinh viên", body)


# ============================================================
# PHẦN 1 - CÂU 4
# LINK RÚT GỌN
# ============================================================

@app.route("/sv/<mssv>")
def short_student(mssv):

    if mssv not in STUDENTS:

        abort(
            404,
            description=f"Không có sinh viên với MSSV = {mssv}."
        )

    return redirect(
        url_for(
            "student_detail",
            mssv=mssv
        ),
        code=301
    )


# ============================================================
# PHẦN 1 - CÂU 5
# XUẤT CSV
# ============================================================

@app.route("/students/<mssv>/export")
def export_scores(mssv):

    if mssv not in STUDENTS:

        abort(
            404,
            description=f"Không có sinh viên với MSSV = {mssv}."
        )

    student = STUDENTS[mssv]

    lines = [
        "hoc_phan,diem"
    ]

    for course, score in student["scores"].items():

        lines.append(
            f"{course},{score}"
        )

    csv_content = "\n".join(lines)

    response = make_response(csv_content)

    response.headers["Content-Type"] = (
        "text/csv; charset=utf-8"
    )

    response.headers["Content-Disposition"] = (
        f"attachment; filename=diem_{mssv}.csv"
    )

    return response


# ============================================================
# PHẦN 1 - CÂU 6
# TÌM KIẾM
# ============================================================

@app.route("/search")
def search():

    keyword = request.args.get("q", "")

    keyword_lower = keyword.lower()

    results = []

    if keyword:

        for mssv, student in STUDENTS.items():

            if (
                keyword_lower in student["name"].lower()
                or keyword_lower in mssv.lower()
            ):

                results.append(
                    student_summary(mssv)
                )

    rows = ""

    for student in results:

        rows += f"""
        <li>
            <a href="{url_for(
                'student_detail',
                mssv=student['mssv']
            )}">
                {escape(student['mssv'])}
                -
                {escape(student['name'])}
            </a>
        </li>
        """

    if keyword:

        result_text = f"""
            <p>
                Tìm thấy
                <strong>{len(results)}</strong>
                kết quả cho
                “{escape(keyword)}”
            </p>
        """

        if results:

            result_text += f"""
                <ul>
                    {rows}
                </ul>
            """

        else:

            result_text += """
                <p>Không tìm thấy sinh viên.</p>
            """

    else:

        result_text = """
            <p>Nhập từ khóa để tìm kiếm.</p>
        """

    body = f"""
        <h1>Tìm kiếm sinh viên</h1>

        <form method="get"
              action="{url_for('search')}">

            <input
                type="text"
                name="q"
                value="{escape(keyword)}"
                placeholder="Nhập MSSV hoặc họ tên"
            >

            <button type="submit">
                Tìm kiếm
            </button>

        </form>

        {result_text}
    """

    return layout("Tìm kiếm", body)


# ============================================================
# PHẦN 2 - CÂU 7
# API ĐỌC DỮ LIỆU
# ============================================================

@app.route("/api/students")
def api_students():

    lop_filter = request.args.get("lop")

    min_avg_raw = request.args.get("min_avg")

    min_avg = None

    # Phân biệt:
    # - không truyền min_avg
    # - truyền min_avg nhưng sai kiểu

    if min_avg_raw is not None:

        try:
            min_avg = float(min_avg_raw)

        except ValueError:

            return (
                {
                    "error": "Dữ liệu không hợp lệ",
                    "detail": "min_avg phải là một số."
                },
                400
            )

    result = []

    for mssv, student in STUDENTS.items():

        summary = student_summary(mssv)

        if lop_filter:

            if student["lop"].lower() != lop_filter.lower():
                continue

        if min_avg is not None:

            if summary["average"] is None:
                continue

            if summary["average"] < min_avg:
                continue

        result.append(summary)

    response = make_response(
        json.dumps(
            result,
            ensure_ascii=False
        )
    )

    response.headers["Content-Type"] = (
        "application/json; charset=utf-8"
    )

    return response


# ============================================================
# API CHI TIẾT SINH VIÊN
# ============================================================

@app.route("/api/students/<mssv>")
def api_student_detail(mssv):

    if mssv not in STUDENTS:

        abort(
            404,
            description=f"Không có sinh viên với MSSV = {mssv}."
        )

    response = make_response(
        json.dumps(
            student_summary(mssv),
            ensure_ascii=False
        )
    )

    response.headers["Content-Type"] = (
        "application/json; charset=utf-8"
    )

    return response



# ============================================================
# CHẠY ỨNG DỤNG
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000
    )