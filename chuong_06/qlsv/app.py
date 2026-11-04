from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
# (1) Định nghĩa lớp cơ sở DeclarativeBase cho các Model về sau kế thừa (db.Model)
class Base(DeclarativeBase):
    pass

# (2) Khởi tạo đối tượng SQLAlchemy kết nối với lớp Base
db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

# Cấu hình Secret Key để bảo mật cho Form/Session
app.config["SECRET_KEY"] = "dev-chi-dung-khi-phat-trien"

# (3) Cấu hình chuỗi kết nối Database (URI)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///qlsv.db"

# (4) Gắn đối tượng db vào ứng dụng Flask
db.init_app(app)

class Student(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    mssv: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    gpa: Mapped[float] = mapped_column(default=0.0)

    def __repr__(self):
        return f"<Student {self.mssv} {self.name}>"

with app.app_context():
    db.create_all()

@app.get("/them-mau")
def add_sample():
    # Kiểm tra xem đã có dữ liệu trong bảng Student chưa
    total = db.session.scalar(
        db.select(func.count(Student.id))
    )
    if total > 0:
        return f"Đã có {total} sinh viên, không thêm nữa."

    # Khởi tạo đối tượng Student cho sinh viên Nguyễn Văn An
    an = Student(
        mssv="23T1020001", 
        name="Nguyễn Văn An", 
        gpa=8.5
    )
    before = an.id  # id lúc này là None (chưa ghi xuống CSDL)
    
    db.session.add(an)  # Đưa vào "giỏ" chờ ghi
    
    # Thêm nhiều sinh viên cùng lúc bằng db.session.add_all()
    db.session.add_all([
        Student(mssv="23T1020002", name="Trần Thị Bình", gpa=6.8),
        Student(mssv="23T1020003", name="Lê Hoàng Cường", gpa=9.1),
        Student(mssv="23T1020004", name="Phạm Minh Dũng", gpa=4.5),
        Student(mssv="23T1020005", name="Hoàng Thu Hà", gpa=7.4),
    ])
    
    db.session.commit()  # Ghi thật sự tất cả vào CSDL
    
    return (f"Đã thêm 5 sinh viên. id của An: "
            f"trước commit = {before}, "
            f"sau commit = {an.id}")
@app.get("/thu-truy-van")
def try_queries():
    # Kiểm tra nếu bảng chưa có dữ liệu thì thông báo nhắc mở /them-mau trước
    if db.session.scalar(
        db.select(func.count(Student.id))
    ) == 0:
        return "Chưa có dữ liệu, hãy mở /them-mau trước."
    
    lines = []
    
    # 1. Truy vấn theo khóa chính (Primary Key) sử dụng .get()
    lines.append(f"1. get(3): {db.session.get(Student, 3)}")
    lines.append(f"2. get(99): {db.session.get(Student, 99)}")  # Không có trả về None
    
    # 3. Lấy tất cả danh sách sinh viên trong bảng
    everyone = db.session.execute(
        db.select(Student)
    ).scalars().all()
    lines.append(f"3. Tất cả: {len(everyone)} sinh viên")
    
    # 4. Truy vấn có điều kiện (.where), sắp xếp giảm dần (.order_by(...desc()))
    stmt = (
        db.select(Student)
        .where(Student.gpa >= 8)
        .order_by(Student.gpa.desc())
    )
    good = db.session.execute(stmt).scalars().all()
    lines.append(f"4. Điểm >= 8: {good}")
    
    # 5. Lọc theo điều kiện cụ thể (.filter_by)
    binh = db.session.scalar(
        db.select(Student)
        .filter_by(mssv="23T1020002")
    )
    lines.append(f"5. MSSV 23T1020002: {binh}")
    
    # 6. Tính toán tổng số lượng và điểm trung bình chung (Aggregate functions)
    count = db.session.scalar(
        db.select(func.count(Student.id))
    )
    avg = db.session.scalar(
        db.select(func.avg(Student.gpa))
    )
    lines.append(f"6. Số SV: {count}, điểm TB: {avg:.2f}")
    
    # Trả về kết quả dưới dạng văn bản thuần (text/plain)
    return "\n".join(lines), {"Content-Type": "text/plain; charset=utf-8"}
from flask import Flask, render_template

# ... (các phần cấu hình và khai báo Model Student đã có trước đó)
@app.get("/danh-sach-sv")
def render_student_table():
    # 1. Truy vấn lấy tất cả sinh viên từ cơ sở dữ liệu
    students = db.session.execute(
        db.select(Student)
    ).scalars().all()
    
    # 2. Render ra file HTML và truyền dữ liệu sang
    return render_template("students.html", students=students)