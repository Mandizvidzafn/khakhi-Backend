from flask import Blueprint, render_template, redirect, request

admin = Blueprint("admin", __name__)


@admin.route("/admin", methods=["GET", "POST"])
def index():
    return render_template("admin/index.html")
