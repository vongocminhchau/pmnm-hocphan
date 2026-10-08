from flask import Flask, render_template, jsonify, request, abort

app = Flask(__name__)

# Danh sách sách
BOOKS = [
    {
        "id": 1,
        "title": "Lập trình Python cơ bản",
        "author": "Nguyễn Văn A",
        "year": 2024,
        "category": "Lập trình",
        "available": True
    },
    {
        "id": 2,
        "title": "Flask Web Development",
        "author": "Miguel Grinberg",
        "year": 2023,
        "category": "Lập trình",
        "available": True
    },
    {
        "id": 3,
        "title": "Cơ sở dữ liệu",
        "author": "Trần Văn B",
        "year": 2022,
        "category": "Cơ sở dữ liệu",
        "available": False
    },
    {
        "id": 4,
        "title": "Nhập môn trí tuệ nhân tạo",
        "author": "Lê Văn C",
        "year": 2024,
        "category": "Trí tuệ nhân tạo",
        "available": True
    },
    {
        "id": 5,
        "title": "HTML và CSS cơ bản",
        "author": "Phạm Văn D",
        "year": 2023,
        "category": "Web",
        "available": True
    }
]


# Tìm sách theo ID
def find_book(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return None


# =========================
# TRANG CHỦ
# =========================
@app.route("/")
def index():
    total_books = len(BOOKS)
    available_books = sum(1 for book in BOOKS if book["available"])

    return render_template(
        "index.html",
        total_books=total_books,
        available_books=available_books
    )


# =========================
# DANH SÁCH SÁCH
# =========================
@app.route("/books")
def books():
    category = request.args.get("category")

    if category:
        filtered_books = [
            book for book in BOOKS
            if book["category"] == category
        ]
    else:
        filtered_books = BOOKS

    categories = sorted(set(book["category"] for book in BOOKS))

    return render_template(
        "books.html",
        books=filtered_books,
        categories=categories,
        selected_category=category
    )


# =========================
# CHI TIẾT SÁCH
# =========================
@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = find_book(book_id)

    if book is None:
        abort(404, description=f"Không có sách với ID = {book_id}")

    return render_template(
        "book_detail.html",
        book=book
    )


# =========================
# API DANH SÁCH SÁCH
# =========================
@app.route("/api/books")
def api_books():
    return jsonify(BOOKS)


# =========================
# API CHI TIẾT SÁCH
# =========================
@app.route("/api/books/<int:book_id>")
def api_book_detail(book_id):
    book = find_book(book_id)

    if book is None:
        return jsonify({
            "error": f"Không có sách với ID = {book_id}"
        }), 404

    return jsonify(book)


# =========================
# TRANG 404
# =========================
@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "404.html",
        error=error
    ), 404


if __name__ == "__main__":
    app.run(debug=True)