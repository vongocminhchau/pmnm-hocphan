## Danh sách Endpoint

| Endpoint | Methods | Rule |
|---|---|---|
| api_get_student_detail | GET | `/api/students/<mssv>` |
| api_get_students | GET | `/api/students` |
| api_manage_score | DELETE, GET, PUT | `/api/students/<mssv>/scores/<course>` |
| export_csv | GET | `/students/<mssv>/export` |
| home | GET | `/` |
| search_student | GET | `/search` |
| short_student_detail | GET | `/sv/<mssv>` |
| static | GET | `/static/<path:filename>` |
| student_detail | GET | `/students/<mssv>` |
| student_list | GET | `/students` |

**Base URL:**

```bash
B=http://127.0.0.1:8000
```

---

## 1. Chuyển hướng 301

```bash
curl -i $B/sv/23T1020001
```

```http
HTTP/1.1 301 MOVED PERMANENTLY
Server: Werkzeug/3.1.9 Python/3.14.6
Date: Wed, 07 Oct 2026 12:05:18 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 227
Location: /students/23T1020001
Connection: close

<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="/students/23T1020001">/students/23T1020001</a>. If not, click the link.
```

---

## 2. Xuất file CSV

```bash
curl -i $B/students/23T1020001/export
```

```http
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.6
Date: Wed, 07 Oct 2026 12:06:44 GMT
Content-Type: text/csv; charset=utf-8
Content-Length: 40
Content-Disposition: attachment; filename=diem_23T1020001.csv
Connection: close

hoc_phan,diem
PMMNM,8.5
CSDL,7.0
MMT,9.0
```

---

## 3. API lọc sinh viên

```bash
curl -i "$B/api/students?lop=k47a&min_avg=7"
```

```http
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.6
Date: Wed, 07 Oct 2026 12:07:54 GMT
Content-Type: application/json
Content-Length: 219
Connection: close

[
  {
    "average": 8.17,
    "lop": "K47A",
    "mssv": "23T1020001",
    "name": "Nguyễn Văn An",
    "rank": "Khá",
    "scores": {
      "CSDL": 7.0,
      "MMT": 9.0,
      "PMMNM": 8.5
    }
  }
]
```

---

## 4. Kiểm tra lỗi 400 (min_avg sai kiểu)

```bash
curl -i "$B/api/students?min_avg=abc"
```

```http
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.9 Python/3.14.6
Date: Wed, 07 Oct 2026 12:19:00 GMT
Content-Type: application/json
Content-Length: 114
Connection: close

{
  "detail": "Tham số min_avg phải là một số hợp lệ.",
  "error": "Dữ liệu không hợp lệ"
}
```

---

## 5. Kiểm tra lỗi 404 (không tìm thấy MSSV)

```bash
curl -i $B/api/students/999
```

```http
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/3.1.9 Python/3.14.6
Date: Wed, 07 Oct 2026 12:19:00 GMT
Content-Type: application/json
Content-Length: 97
Connection: close

{
  "detail": "Không tìm thấy sinh viên có MSSV = 999.",
  "error": "Không tìm thấy"
}
```

---

## 6. Thêm điểm mới (Trả về 201 + Header Location)

```bash
S=$B/api/students/23T1020005/scores
curl -i -X PUT "$S/web?score=9"
```

```http
HTTP/1.1 201 CREATED
Server: Werkzeug/3.1.9 Python/3.14.6
Date: Wed, 07 Oct 2026 12:19:00 GMT
Content-Type: application/json
Content-Length: 80
Location: /api/students/23T1020005/scores/WEB
Connection: close

{
  "average": 9.0,
  "course": "WEB",
  "mssv": "23T1020005",
  "score": 9.0
}
```

---

## 7. Sửa điểm đã có (Trả về 200)

```bash
curl -i -X PUT "$S/WEB?score=7.5"
```

```http
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.6
Date: Wed, 07 Oct 2026 12:19:00 GMT
Content-Type: application/json
Content-Length: 80
Connection: close

{
  "average": 7.5,
  "course": "WEB",
  "mssv": "23T1020005",
  "score": 7.5
}
```

---

## 8. Lỗi điểm vượt quá khoảng [0, 10] (Trả về 400)

```bash
curl -i -X PUT "$S/WEB?score=11"
```

```http
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.9 Python/3.14.6
Date: Wed, 07 Oct 2026 12:19:00 GMT
Content-Type: application/json
Content-Length: 116
Connection: close

{
  "detail": "Điểm phải nằm trong khoảng từ 0 đến 10.",
  "error": "Dữ liệu không hợp lệ"
}
```

---

## 9. Xóa điểm (Trả về 204)

```bash
curl -i -X DELETE $S/WEB
```

```http
HTTP/1.1 204 NO CONTENT
Server: Werkzeug/3.1.9 Python/3.14.6
Date: Wed, 07 Oct 2026 12:19:00 GMT
Content-Type: text/html; charset=utf-8
Connection: close
```

---

## 10. Lỗi phương thức POST không hỗ trợ (Trả về 405)

```bash
curl -i -X POST $S/WEB
```

```http
HTTP/1.1 405 METHOD NOT ALLOWED
Server: Werkzeug/3.1.9 Python/3.14.6
Date: Wed, 07 Oct 2026 12:19:00 GMT
Content-Type: application/json
Content-Length: 124
Connection: close

{
  "detail": "The method is not allowed for the requested URL.",
  "error": "Phương thức không được hỗ trợ"
}
```

```bash
curl -i -X POST $B/students
```

```http
HTTP/1.1 405 METHOD NOT ALLOWED
Server: Werkzeug/3.1.9 Python/3.14.6
Date: Wed, 07 Oct 2026 12:19:00 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 449
Connection: close

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Lỗi 405 - Sổ điểm</title>
</head>
<body>
    <nav>
        <a href="/">Trang chủ</a> |
        <a href="/students">Sinh viên</a> |
        <a href="/search">Tìm kiếm</a>
    </nav>
    <hr>
    <h1>Lỗi 405</h1>
    <div><h2>405 - Phương thức không được hỗ trợ</h2><p>The method is not allowed for the requested URL.</p></div>
</body>
</html>
```

---

# Câu hỏi và trả lời

## Vì sao Câu 4 dùng 301 còn Câu 8 trả 201 kèm Location?

**Mã 301 (Moved Permanently):** Sử dụng cho route chuyển hướng rút gọn `/sv/<mssv>` về `/students/<mssv>` nhằm thông báo cho trình duyệt và máy tìm kiếm rằng tài nguyên này đã được di chuyển vĩnh viễn sang địa chỉ URL chính thức.

**Mã 201 (Created):** Sử dụng khi tạo mới thành công một điểm học phần bằng phương thức PUT. Header `Location` đi kèm trỏ trực tiếp tới URL của điểm học phần vừa tạo để tuân thủ đúng chuẩn thiết kế RESTful API.

---

## Thêm điểm cho 23T1020005 rồi khởi động lại server, điểm đó còn không? Vì sao?

**Trả lời:** Không còn.

**Lý do:** Dữ liệu `STUDENTS` hiện tại chỉ được lưu tạm thời trên bộ nhớ RAM dưới dạng một biến dictionary trong Python. Khi khởi động lại server Flask, tiến trình chạy ứng dụng bị ngắt và khởi chạy lại, dẫn đến bộ nhớ RAM bị giải phóng và dữ liệu được khôi phục về trạng thái mặc định ban đầu.