from flask import Blueprint, render_template, request, redirect, session
from dataclasses import asdict
import messages.error_list as el
import messages.success_list as sl
import db as db 
import sqlite3
import globals.globals as gl
import bcrypt
from dataclasses import dataclass, field
import db.login_db as l_db
from typing import Optional

login = Blueprint("login", __name__)

@login.get("/login")
def user_login_page():
    error = None 
    success = None 
    error_key = request.args.get("error", None)
    success_key =  request.args.get("success", None)
    if error_key is not None:
        error = el.ErrorList.get(error_key)
    if success_key is not None:
        success = sl.SuccessList.get(success_key)
    return render_template("/login.jinja",
                           error=error, success=success)
    
@login.post("/login")
def login_submission():
    try:
        user_data = request.form 
        print(user_data["username"])
        print(user_data["password"])
        user = l_db.login_(user_data["username"], user_data["password"])
        if user == False:
            return redirect("/login?error=invalid_credentials")
        else:
            session["user"] = user
        return redirect("/index_stock?success=login_success")
    except sqlite3.OperationalError:
        return redirect("/login?error=vec_ste_ulogovani")
    
@login.get("/logout")
def logout():
        del session["user"]
        return redirect("/?success=logout_success")