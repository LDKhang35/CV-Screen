from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    print("Template folder Flask đang tìm:", app.template_folder)
    app.config.from_object('config.Config')

    db.init_app(app)
    Migrate(app, db)

    from .routes.main import main_bp
    from app.routes.results import results_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(results_bp)

    return app
