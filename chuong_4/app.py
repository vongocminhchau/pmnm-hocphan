
from flask import Blueprint, Flask, render_template, request

menu_blueprint = Blueprint("menu", __name__)

MENU = [
    {"name": "cà phê đen", "price": 20000, "available": True},
    {"name": "bạc xỉu", "price": 30000, "available": False},
    {"name": "cà phê sữa", "price": 40000, "available": True},
    {"name": "trà đào", "price": 25000, "available": True},
    {"name": "matcha latte", "price": 35000, "available": True}
]


# Bộ lọc định dạng giá tiền Việt Nam
@menu_blueprint.app_template_filter("vnd")
def vnd(price):
    return f"{price:,.0f}".replace(",", ".") + " đ"


@menu_blueprint.get("/menu")
def menu():
    # Thử trường hợp thực đơn rỗng bằng /menu?empty=1
    items = [] if request.args.get("empty") == "1" else MENU

    # Tính giá trung bình
    average_price = (
        sum(item["price"] for item in items) / len(items)
        if items else 0
    )

    # Đếm số món đang có
    available_count = sum(
        1 for item in items if item["available"]
    )

    return render_template(
        "menu.html",
        menu=items,
        average_price=average_price,
        available_count=available_count
    )


if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(menu_blueprint)
    app.run(debug=True)
