from flask import Blueprint, render_template
from ...admin.models import Product

customer_view_routes = Blueprint('customer_view_routes', __name__)

@customer_view_routes.route('/', methods=['GET', 'POST'])
def index():
    products = Product.query.all()
    return render_template("customer/index.html", products=products)
