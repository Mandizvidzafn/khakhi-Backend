from flask import Blueprint, render_template, redirect, request

products = Blueprint("products", __name__)


@products.route("/order", methods=["GET", "POST"])
def order():
    return render_template("admin/order.html")


@products.route("/category", methods=["GET", "POST"])
def category():
    return render_template("admin/category.html")


@products.route("/product", methods=["GET", "POST"])
def product():
    return render_template("admin/product.html")


@products.route("/stock", methods=["GET", "POST"])
def stock():
    return render_template("admin/stock.html")
