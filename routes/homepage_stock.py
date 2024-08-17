from flask import Blueprint, render_template, session, request
import messages.success_list as sl
import db.homepage_db as db_h
import db as db 


homepage_stock_blueprint = Blueprint("homepage_stock", __name__)

@homepage_stock_blueprint.get("/index_stock")
def user_homepage_magacin():
    success = None 
    success_key = request.args.get("success", None)
    if success_key is not None:
        success = sl.SuccessList.get(success_key)
    carpets = db_h.get_carpets_for_display()
    return render_template("index_stock.jinja",
                           success=success, carpets=carpets)