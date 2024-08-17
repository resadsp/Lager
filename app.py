from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from pathlib import Path
from dotenv import load_dotenv
from routes.homepage import homepage
from routes.homepage_stock import homepage_stock_blueprint
from routes.login import login
from routes.admin import admin
import os

load_dotenv()

parent_dir = Path(__file__).parent
templates_folder = parent_dir / "templates"
static_folder = parent_dir / "static"

app = Flask(__name__, static_folder=static_folder,
            static_url_path="/static",
            template_folder=templates_folder)

app.secret_key = "18b3c871d7fb606463b0dfd367e4036456"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(homepage)
app.register_blueprint(homepage_stock_blueprint)
app.register_blueprint(login)
app.register_blueprint(admin)

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        debug=os.getenv("DEBUG")
    )
    