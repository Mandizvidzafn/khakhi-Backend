from flask import Blueprint, render_template

view = Blueprint("view", __name__)


@view.route("/", methods=["GET", "POST"])
def index():
    name = "Henny"
    return render_template("index.html")


@view.route("/account", methods=["GET", "POST"])
def account():
    return render_template("account.html")


@view.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")


@view.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")


@view.route("/shop", methods=["GET", "POST"])
def shop():
    return render_template("shop.html")
