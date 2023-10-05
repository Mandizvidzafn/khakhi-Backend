from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from project import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    sku = db.Column(db.String(50), nullable=False, default="WH000")
    price = db.Column(db.Float, nullable=False)
    categories = db.relationship('Category', secondary='product_category', backref='products')
    category_types = db.relationship('Category_type', secondary='product_category_type', backref='products')
    quantity = db.Column(db.Integer, default=0)
    description = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(20), nullable=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Product('{self.id}', '{self.name}', '{self.categories}', '{self.category_types}', '{self.date_added}')"
    
product_category = db.Table('product_category',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)


product_category_type = db.Table('product_category_type',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('category_type_id', db.Integer, db.ForeignKey('category_type.id'), primary_key=True)
)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    cat_type = db.Column(db.String, db.ForeignKey('category_type.name'))


class Category_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

