
from datetime import datetime
from flask import Flask, render_template, request

from app import SHOP, menu_blueprint

app = Flask(__name__)
app.register_blueprint(menu_blueprint)

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
        hour=hour,
        is_open=is_open,
        promotions=PROMOTIONS
    )


@app.get("/contact")
def contact():
    return render_template("contact.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
