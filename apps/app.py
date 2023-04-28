from flask import Flask
from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_key):
    #Flaskインスタンス作成
    app = Flask(__name__)
    #アプリのコンフィグ設定をする
    app.config.from_object(config[config_key])

    db.init_app(app)

    csrf.init_app(app)

    Migrate(app, db)
    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app