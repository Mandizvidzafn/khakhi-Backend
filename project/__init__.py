from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path

db_NAME = "khakhi.db"
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "hsjaggi dah dgaha"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_NAME}"
    db.init_app(app)
    migrate.init_app(app)

    from project.views.views import view
    from project.auth.customer import customer
    from project.auth.admin import admin
    from project.products.product import products

    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(customer)
    app.register_blueprint(admin)
    app.register_blueprint(products)

    create_database(app)

    return app


def create_database(app):
    if not path.exists("project/" + db_NAME):
        with app.app_context():
            db.create_all()
            print("Created Database")
