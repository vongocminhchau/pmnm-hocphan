
from flask import Blueprint, abort, render_template, request

menu_blueprint = Blueprint("menu", __name__)

SHOP = {
    "name": "Cà phê Sông Hương",
    "short_name": "Sông Hương",
    "address": "12 Lê Lợi, Huế",
    "phone": "0234 3888 999",
    "open": 7,
    "close": 22,
}

MENU = [
    {"id": 1, "name": "cà phê đen", "price": 20000, "image": "ca-phe-den.jpg", "available": True},
    {"id": 2, "name": "cà phê sữa", "price": 40000, "image": "ca-phe-sua.jpg", "available": True},
    {"id": 3, "name": "bạc xỉu", "price": 30000, "image": "bac-xiu.jpg", "available": False},
    {"id": 4, "name": "trà đào", "price": 25000, "image": "tra-dao.jpg", "available": True},
    {"id": 5, "name": "trà sữa", "price": 35000, "image": "tra-sua.jpg", "available": True},
    {"id": 6, "name": "nước cam", "price": 30000, "image": "nuoc-cam.jpg", "available": True},
    {"id": 7, "name": "sinh tố bơ", "price": 45000, "image": "sinh-to-bo.jpg", "available": True},
]


@menu_blueprint.app_context_processor
def inject_shop():
    return {"shop": SHOP}


# Bộ lọc định dạng giá tiền Việt Nam
@menu_blueprint.app_template_filter("vnd")
def vnd(price):
    return f"{price:,.0f}".replace(",", ".") + " đ"


@menu_blueprint.get("/menu")
def menu():
    all_items = [] if request.args.get("empty") == "1" else MENU
    per_page = 3
    pages = max(1, (len(all_items) + per_page - 1) // per_page)
    page = request.args.get("page", default=1, type=int)

    if page < 1 or page > pages:
        abort(404)

    start = (page - 1) * per_page
    items = all_items[start:start + per_page]
    average_price = (
        sum(item["price"] for item in all_items) / len(all_items)
        if all_items else 0
    )
    available_count = sum(1 for item in all_items if item["available"])

    return render_template(
        "menu.html",
        menu=items,
        page=page,
        pages=pages,
        total_items=len(all_items),
        average_price=average_price,
        available_count=available_count
    )


if __name__ == "__main__":
    from cafe import app

    app.run(debug=True)
