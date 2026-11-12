

from flask import Flask, render_template, request, redirect, url_for, flash, abort
from models import db, Category, Book
from sqlalchemy import func

app = Flask(__name__, instance_relative_config=True)

# Cấu hình ứng dụng
app.config["SECRET_KEY"] = "dev-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book_manager.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Kết nối SQLAlchemy với Flask
db.init_app(app)


# Tạo bảng nếu chưa tồn tại
with app.app_context():
    db.create_all()

# ==============================
# DASHBOARD
# ==============================


@app.route("/")
@app.route("/dashboard")
def dashboard():
    total_books = db.session.scalar(
        db.select(func.count(Book.id))
    ) or 0

    total_quantity = db.session.scalar(
        db.select(func.coalesce(func.sum(Book.quantity), 0))
    ) or 0

    total_categories = db.session.scalar(
        db.select(func.count(Category.id))
    ) or 0

    low_stock_books = db.session.scalar(
        db.select(func.count(Book.id)).where(
            Book.quantity.between(1, 5)
        )
    ) or 0

    recent_books = db.session.execute(
        db.select(Book).order_by(Book.id.desc()).limit(5)
    ).scalars().all()

    return render_template(
        "dashboard.html",
        total_books=total_books,
        total_quantity=total_quantity,
        total_categories=total_categories,
        low_stock_books=low_stock_books,
        recent_books=recent_books
    )



# ==============================
# CATEGORY - READ
# ==============================

@app.route("/categories")
def category_index():
    categories = db.session.execute(
        db.select(Category).order_by(Category.id.desc())
    ).scalars().all()

    return render_template(
        "categories/index.html",
        categories=categories
    )


# ==============================
# CATEGORY - CREATE
# ==============================

@app.route("/categories/create", methods=["GET", "POST"])
def category_create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("Tên danh mục không được để trống.", "danger")
            return render_template("categories/create.html")

        existing = db.session.scalar(
            db.select(Category).filter_by(name=name)
        )

        if existing:
            flash("Tên danh mục đã tồn tại.", "warning")
            return render_template("categories/create.html")

        category = Category(
            name=name,
            description=description
        )

        try:
            db.session.add(category)
            db.session.commit()
            flash("Thêm danh mục thành công!", "success")
            return redirect(url_for("category_index"))

        except Exception:
            db.session.rollback()
            flash("Có lỗi xảy ra khi thêm danh mục.", "danger")

    return render_template("categories/create.html")


# ==============================
# CATEGORY - UPDATE
# ==============================

@app.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
def category_edit(category_id):
    category = db.get_or_404(Category, category_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("Tên danh mục không được để trống.", "danger")
            return render_template(
                "categories/edit.html",
                category=category
            )

        existing = db.session.scalar(
            db.select(Category).where(
                Category.name == name,
                Category.id != category.id
            )
        )

        if existing:
            flash("Tên danh mục đã được sử dụng.", "warning")
            return render_template(
                "categories/edit.html",
                category=category
            )

        category.name = name
        category.description = description

        try:
            db.session.commit()
            flash("Cập nhật danh mục thành công!", "success")
            return redirect(url_for("category_index"))

        except Exception:
            db.session.rollback()
            flash("Có lỗi xảy ra khi cập nhật.", "danger")

    return render_template(
        "categories/edit.html",
        category=category
    )


# ==============================
# CATEGORY - DELETE
# ==============================

@app.route("/categories/<int:category_id>/delete", methods=["POST"])
def category_delete(category_id):
    category = db.get_or_404(Category, category_id)

    if category.books:
        flash(
            "Không thể xóa danh mục đang chứa sách. "
            "Hãy chuyển hoặc xóa các sách thuộc danh mục trước.",
            "warning"
        )
        return redirect(url_for("category_index"))

    try:
        db.session.delete(category)
        db.session.commit()
        flash("Xóa danh mục thành công!", "success")

    except Exception:
        db.session.rollback()
        flash("Có lỗi xảy ra khi xóa danh mục.", "danger")

    return redirect(url_for("category_index"))

# ==============================
# BOOK - READ
# ==============================

@app.route("/books")
def book_index():
    books = db.session.execute(
        db.select(Book).order_by(Book.id.desc())
    ).scalars().all()

    return render_template("books/index.html", books=books)


# ==============================
# BOOK - CREATE
# ==============================

@app.route("/books/create", methods=["GET", "POST"])
def book_create():
    categories = db.session.execute(
        db.select(Category).order_by(Category.name)
    ).scalars().all()

    if not categories:
        flash("Bạn cần tạo danh mục trước khi thêm sách.", "warning")
        return redirect(url_for("category_create"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        publish_year_raw = request.form.get("publish_year", "").strip()
        quantity_raw = request.form.get("quantity", "0").strip()
        category_id_raw = request.form.get("category_id", "").strip()

        if not title or not author:
            flash("Tên sách và tác giả không được để trống.", "danger")
            return render_template(
                "books/create.html", categories=categories
            )

        try:
            publish_year = int(publish_year_raw) if publish_year_raw else None
            quantity = int(quantity_raw)
            category_id = int(category_id_raw)
        except ValueError:
            flash("Năm xuất bản, số lượng hoặc danh mục không hợp lệ.", "danger")
            return render_template(
                "books/create.html", categories=categories
            )

        if (publish_year is not None and publish_year <= 0) or quantity < 0:
            flash("Năm xuất bản phải lớn hơn 0 và số lượng không được âm.", "danger")
            return render_template(
                "books/create.html", categories=categories
            )

        category = db.session.get(Category, category_id)
        if category is None:
            flash("Danh mục được chọn không tồn tại.", "danger")
            return render_template(
                "books/create.html", categories=categories
            )

        book = Book(
            title=title,
            author=author,
            publish_year=publish_year,
            quantity=quantity,
            category=category
        )

        try:
            db.session.add(book)
            db.session.commit()
            flash("Thêm sách thành công!", "success")
            return redirect(url_for("book_index"))

        except Exception:
            db.session.rollback()
            flash("Có lỗi xảy ra khi thêm sách.", "danger")

    return render_template("books/create.html", categories=categories)


# ==============================
# BOOK - UPDATE
# ==============================

@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def book_edit(book_id):
    book = db.get_or_404(Book, book_id)

    categories = db.session.execute(
        db.select(Category).order_by(Category.name)
    ).scalars().all()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        publish_year_raw = request.form.get("publish_year", "").strip()
        quantity_raw = request.form.get("quantity", "0").strip()
        category_id_raw = request.form.get("category_id", "").strip()

        if not title or not author:
            flash("Tên sách và tác giả không được để trống.", "danger")
            return render_template(
                "books/edit.html", book=book, categories=categories
            )

        try:
            publish_year = int(publish_year_raw) if publish_year_raw else None
            quantity = int(quantity_raw)
            category_id = int(category_id_raw)
        except ValueError:
            flash("Năm xuất bản, số lượng hoặc danh mục không hợp lệ.", "danger")
            return render_template(
                "books/edit.html", book=book, categories=categories
            )

        if (publish_year is not None and publish_year <= 0) or quantity < 0:
            flash("Năm xuất bản phải lớn hơn 0 và số lượng không được âm.", "danger")
            return render_template(
                "books/edit.html", book=book, categories=categories
            )

        category = db.session.get(Category, category_id)
        if category is None:
            flash("Danh mục được chọn không tồn tại.", "danger")
            return render_template(
                "books/edit.html", book=book, categories=categories
            )

        book.title = title
        book.author = author
        book.publish_year = publish_year
        book.quantity = quantity
        book.category = category

        try:
            db.session.commit()
            flash("Cập nhật sách thành công!", "success")
            return redirect(url_for("book_index"))

        except Exception:
            db.session.rollback()
            flash("Có lỗi xảy ra khi cập nhật sách.", "danger")

    return render_template(
        "books/edit.html", book=book, categories=categories
    )


# ==============================
# BOOK - DELETE
# ==============================

@app.route("/books/<int:book_id>/delete", methods=["POST"])
def book_delete(book_id):
    book = db.get_or_404(Book, book_id)

    try:
        db.session.delete(book)
        db.session.commit()
        flash("Xóa sách thành công!", "success")

    except Exception:
        db.session.rollback()
        flash("Có lỗi xảy ra khi xóa sách.", "danger")

    return redirect(url_for("book_index"))


if __name__ == "__main__":
    app.run(debug=True)