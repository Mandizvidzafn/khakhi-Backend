from flask import Blueprint, render_template

customer = Blueprint("customer", __name__)


@customer.route("/change-password", methods=["GET", "POST"])
def change_password():
    return render_template("change-password.html")
