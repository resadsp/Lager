from flask import Blueprint, render_template, request
from dataclasses import dataclass, field
from typing import Optional
import db.homepage_db as a_carpets
import messages.success_list as sl
import db as db 
import globals.globals as gl
import db.homepage_db as db_h

    
homepage = Blueprint("homepage", __name__)

@homepage.get("/")
def user_homepage():
    success = None 
    success_key = request.args.get("success", None)
    if success_key is not None:
        success = sl.SuccessList.get(success_key)
    carpets = db_h.get_carpets_for_display()
    return render_template("index.jinja", carpets=carpets, success=success)

