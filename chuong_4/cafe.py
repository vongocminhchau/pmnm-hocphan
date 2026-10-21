
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

SHOP = {
    "name": "Cà phê Sông Hương",
    "address": "12 Lê Lợi, Huế",
    "open": 7,
    "close": 22
}

PROMOTIONS = [
    "Giảm 10% cho sinh viên",
    "Mua 2 tặng 1 vào thứ Hai"
]


@app.get("/")
def index():
    hour = request.args.get("gio", type=int)

    if hour is None:
        hour = datetime.now().hour

    is_open = SHOP["open"] <= hour < SHOP["close"]

    return render_template(
        "index.html",
        shop=SHOP,
        hour=hour,
        is_open=is_open,
        promotions=PROMOTIONS
    )


if __name__ == "__main__":
    app.run(debug=True)
