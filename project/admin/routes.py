from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os
import secrets
from project import db
from .models import Product, Category, Category_type
from uuid import uuid4

admin_routes = Blueprint('admin_routes', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_name(id):
    product = Product.query.get(id)
    image_name = product.image
    return image_name

#add products
@admin_routes.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    categories = Category.query.all()
    categories_types = Category_type.query.all()
    products = Product.query.all()

    if request.method == 'POST':
        name = request.form.get('pname')
        price = request.form.get('price')
        short_desc = request.form.get('sdesc')
        long_desc = request.form.get('ldesc')
        quantity = request.form.get("quantity")
        sku = request.form.get("sku")
        category = request.form.getlist('category')
        category_types = request.form.getlist('category_types')
        image = request.files.get('image')

        if image and allowed_file(image.filename):
            image_name = secure_filename(image.filename)
            unique_img_name = uuid4() + "-" + image_name
            image_path = os.path.join('project', 'static', 'img', 'products', unique_img_name)
            image.save(image_path)
        else:
            image_name = None

        product = Product.query.filter_by(name=name).first()
        if product:
            flash("Product exists", "danger")
        else:
            categories_obj = [Category.query.get(int(cat_id)) for cat_id in category]
            category_types_obj = [Category_type.query.get(int(cat_type_id)) for cat_type_id in category_types]

            #if quantity is empty
            if quantity == "" or None:
                add_product = Product(name=name,
                                      price=price,
                                      description=short_desc,
                                      sku=sku,
                                      categories=categories_obj,
                                      category_types=category_types_obj,
                                      image=image_name)
                db.session.add(add_product)
                db.session.commit()
                
                flash("Product added successfully", "success")
                return redirect(url_for("admin_routes.add_product"))
                
            #if sku is empty
            elif sku == "" or None:
                add_product = Product(name=name,
                                      price=price,
                                      description=short_desc,
                                      quantity=quantity,
                                      categories=categories_obj,
                                      category_types=category_types_obj,
                                      image=image_name)
                db.session.add(add_product)
                db.session.commit()
                
                flash("Product added successfully", "success")
                return redirect(url_for("admin_routes.add_product"))

            #if both quantity and sku is empty
            elif quantity == "" or None and sku == "" or None:
                add_product = Product(name=name,
                                      price=price,
                                      description=short_desc,
                                      categories=categories_obj,
                                      category_types=category_types_obj,
                                      image=image_name)
                db.session.add(add_product)
                db.session.commit()
                
                flash("Product added successfully", "success")
                return redirect(url_for("admin_routes.add_product"))

            #if both are not empty
            else:
                add_product = Product(name=name,
                                      price=price,
                                      description=short_desc,
                                      sku=sku,
                                      quantity= quantity,
                                      categories=categories_obj,
                                      category_types=category_types_obj,
                                      image=image_name)
                db.session.add(add_product)
                db.session.commit()
                
                flash("Product added successfully", "success")
                return redirect(url_for("admin_routes.add_product"))


    return render_template("admin/add_product.html", categories=categories, categories_types=categories_types, products=products)

#view all products
@admin_routes.route('/admin/products', methods=['GET', 'POST'])
def products():
    products = Product.query.all()

    return render_template("admin/products.html", products=products)

@admin_routes.route('/admin/products/<int:id>')
def view_product(id):
    product = Product.query.get(id)

    image_name = get_image_name(product.id)
    image_path = os.path.join(current_app.static_folder, 'img' 'products', image_name)

    return render_template("admin/view_product.html", product=product, image_path=image_path)

#Render te admin dashboard
@admin_routes.route('/admin', methods=['GET', 'POST'])
def index():
    products = Product.query.all()

    return render_template("admin/index.html", products=products)

# Display a form to add new categories and category types
@admin_routes.route('/admin/category', methods=['GET', 'POST'])
def category():
    # Get all existing category types and categories
    category_types = Category_type.query.all()
    categories = Category.query.all()
    if request.method == "POST":
        #Add a new Category Type
        if "addCategorytype" in request.form:
            addcat_type = request.form.get("add_cat_type").lower()

            catType = Category_type.query.filter_by(name=addcat_type).first()
            if not catType:
                if addcat_type != "":
                    print(f"Added: {addcat_type}")
                    add_cat_type = Category_type(name=addcat_type)
                    db.session.add(add_cat_type)
                    db.session.commit()
                    flash(f"Created {addcat_type} category type", "info")
                else: flash("PLease enter the category type", "error")
            else: flash(f"Category Type {addcat_type.upper()} exists", "danger")
            

        #Add Category
        elif "addCategory" in request.form:
            cat_name = request.form.get("cat_name").lower()
            cat_type = request.form.get("cat_type")
            print(f"cat_name: {cat_name} cat_type: {cat_type}")
            category = Category.query.filter_by(name=cat_name).first()
            category_type = Category.query.filter_by(cat_type=cat_type).first()
            if category and category.cat_type == cat_type:
                flash("Category exists", "danger")
            else:
                if cat_name == "" or cat_type == None:
                    flash("Please enter all the details", "danger")
                else:
                    print(f"Cat type: {cat_type}")
                    add_category = Category(name=cat_name,
                                            cat_type=cat_type)
                    #add_category.category_types.append(cat_type)
                    db.session.add(add_category)
                    db.session.commit()
                    flash(f"Category {cat_name.upper()} was added succesfully", "info")
                    return redirect(url_for("admin_routes.category"))

    return render_template("admin/category.html", category_type=category_types, categories=categories)


@admin_routes.route("/admin/stock", methods=['GET', 'POST', 'PATCH'])
def stock():
    products = Product.query.all()
    if request.method == 'POST':
        product_name = request.form.get('pname')
        product_quantity = request.form.get('pqty')
        product = Product.query.filter_by(name=product_name).first()
        print(product)
        if not product:
            flash("Product not found", 'error')
        elif product_quantity == '' or None:
            flash("Please enter product quantity", "danger")     
        else:
            product.quantity += int(product_quantity)
            db.session.commit()
            

    return render_template('admin/stock.html', products=products)

@admin_routes.route('/admin/order', methods=['GET', 'POST'])
def order():
    return render_template("admin/order.html")

@admin_routes.route('/admin/dummy', methods=['GET', 'POST'])
def dummy():
    return render_template("admin/dummy_product.html")