from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
from flask_uploads import UploadSet, IMAGES, configure_uploads

db_NAME = "admin.db"
db = SQLAlchemy()
migrate = Migrate()
basedir = path.abspath(path.dirname(__file__))
photos = UploadSet("photos", IMAGES)


from .admin import models

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "hsjaggi dah dgaha"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_NAME}"
    app.config["UPLOADED_PHOTOS_DEST"] = path.join(basedir, 'static/img/product')
    configure_uploads(app, photos)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    db.init_app(app)
    migrate.init_app(app, db)

    #Creating Database
    create_database(app)
    #Registering Blueprints
    from .admin.routes import admin_routes
    from .customers.views.routes import customer_view_routes
    app.register_blueprint(admin_routes)
    app.register_blueprint(customer_view_routes)

    return app

def create_database(app):
   if not path.exists("khakhi-main/" + db_NAME):
       with app.app_context():
           db.create_all()
    