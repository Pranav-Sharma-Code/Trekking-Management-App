import os
from flask import Flask
from app.config.config import Config
from app.extensions import (
    db, migrate, login_manager, toolbar
)
def create_app():
    app = Flask (
        __name__,
        instance_relative_config=True,
    )

    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    toolbar.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to continue"

    @app.route("/")
    def home():
        return "<h1>Trekking Management Application</h1>"
    return app