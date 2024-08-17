from flask import Blueprint, render_template, session, request, redirect, sessions, send_file
from werkzeug.utils import secure_filename
from jinja2 import Template
from datetime import datetime
from dataclasses import asdict
from functools import wraps
import messages.success_list as sl
import messages.error_list as el
import db.admin_bp as l_login
import db as db 
import pdfkit
import base64
import globals.globals as gl
import os
import math

#redirect - salje i vraca na RUTE
#render_template - salje na STRANICE

admin = Blueprint("admin", __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin.before_request
def check_admin_rights():
    if not "user" in session:
        return redirect("/login?error=administrator")

@admin.get("/search")
def search_get():
    error = None 
    success = None 
    error_key = request.args.get("error", None)
    success_key =  request.args.get("success", None)
    if error_key is not None:
        error = el.ErrorList.get(error_key)
    if success_key is not None:
        success = sl.SuccessList.get(success_key)
    return render_template("search.jinja",
                           error=error, success=success)

@admin.get("/individual_view")
def individual_view_get():
    if "sifra" in request.args.keys():
        sifra = request.args["sifra"]
    error = None 
    success = None 
    error_key = request.args.get("error", None)
    success_key =  request.args.get("success", None)
    if error_key is not None:
        error = el.ErrorList.get(error_key)
    if success_key is not None:
        success = sl.SuccessList.get(success_key)
    user_data = request.form 
    if "sifra" in request.args.keys():
        sifra = request.args["sifra"]
    else:
        sifra =  user_data["sifra"]
    user = l_login.find_in_stock_pass(sifra)
    user = list(user)
    if user:
        return render_template("individual_view.jinja", user=user)
    else:
        return redirect("/search?error=something")
      
@admin.get("/input")
def input_get():
    error = None 
    error_key = request.args.get("error", None)
    if error_key is not None:
        error = el.ErrorList.get(error_key)
    return render_template("input.jinja", error = error)

@admin.post("/input")
def input_post():
    kolekcija = request.form.get("kolekcija")
    sifra = request.form.get("sifra")
    D80x150 = int(request.form.get("D80x150"))
    D80x300  = int(request.form.get("D80x300"))
    D120x200  = int(request.form.get("D120x200"))
    D160x230  = int(request.form.get("D160x230"))
    D200x300 = int(request.form.get("D200x300"))
    D120x120  = int(request.form.get("D120x120"))
    D160x160  = int(request.form.get("D160x160"))
    D200x200 = int(request.form.get("D200x200"))
    slika1 = request.files["slika1"]
    kvadratura =  D80x150 * 1.2 +  D80x300 * 2.4 + D120x200 * 2.4 + D160x230 * 3.76 + D200x300 * 6 + D120x120 * 1.44 + D160x160 * 2.56 + D200x200 * 4
    kvadratura = round(kvadratura, 2)
    br = 1
    if slika1 and allowed_file(slika1.filename):
                    br += 1
    try:
        if br == 2:
            is_saved_tepisi = l_login.save_carpet(kolekcija, sifra, D80x150, D80x300, D120x200, D160x230, D200x300, slika1.filename, kvadratura, D120x120, D160x160, D200x200)
        else:
            return redirect("/input?error=format")
        if is_saved_tepisi>0:
                if slika1 and allowed_file(slika1.filename):
                    filename = secure_filename(slika1.filename)
                    slika1.save(os.path.join("./static/img", filename))
                return redirect("/index_stock?success=tepih_saved")
        else:
             return redirect("/?error=tepih_saving")
    except Exception:
             return redirect("/input?error=vec_postoji")
    
@admin.get("/update/<string:sifra>")
def update_get(sifra: str):
    i = l_login.find_in_stock_pass(sifra)
    if i:
          return render_template("update.jinja", i=i) 
    else:
        print (i)
        return redirect("/?error=tepih_saving") 
    
@admin.get("/view")
def view_get():
    cela = l_login.find_in_stock()
    if cela:
        return render_template("view.jinja", cela=cela)
    else: 
        return redirect("/search?error=something")
    
@admin.get("/printing")
def printing_get():
    cela = l_login.find_in_stock()
    with open("./templates/printing.jinja", "r", encoding="utf-8") as f:
        with open("./static/assets/logobalta.jpg", "rb") as img:
            imgb64 = base64.b64encode(img.read()).decode("utf-8")
        t = Template(f.read())
        pdf_name = "./stock/" + datetime.strftime(datetime.now(), "%Y_%m_%d__%H_%M_%S_-_BAZA.pdf")
        pdfkit.from_string(t.render(
            report_timestamp=str(datetime.strftime(datetime.now(),'%d.%m.%Y-%H:%M:%S')),
cela=cela, company_logo=imgb64), pdf_name)
    if cela:
        return send_file(pdf_name, as_attachment=True)
    else: 
        return redirect("/search?error=something")
    
@admin.get("/printing_saldo")
def printing_get_saldo():
    s=0
    izvestaj = l_login.find_saldo()
    for i in izvestaj:
        s += i[1]
    with open("./templates/printing_saldo.jinja", "r", encoding="utf-8") as f:
        with open("./static/assets/logobalta.jpg", "rb") as img:
            imgb64 = base64.b64encode(img.read()).decode("utf-8")
        t = Template(f.read())
        pdf_name = "./stock/" + datetime.strftime(datetime.now(), "%Y_%m_%d__%H_%M_%S_- MESECNI IZVESTAJ.pdf")
        pdfkit.from_string(t.render(
            report_timestamp=str(datetime.strftime(datetime.now(),'%d.%m.%Y-%H:%M:%S')),
izvestaj=izvestaj, s=s, company_logo=imgb64), pdf_name)
    if izvestaj:
        return send_file(pdf_name, as_attachment=True)
    else: 
        return redirect("/search?error=something")
    
@admin.get("/printing_metres")
def printing_get_metres():
    sardes = gl.GlobalComponents.get("sardes")
    gaspara = gl.GlobalComponents.get("gaspara")
    allures = gl.GlobalComponents.get("allures")
    erva = gl.GlobalComponents.get("erva")
    rivenna = gl.GlobalComponents.get("rivenna")
    s = gl.GlobalComponents.get("s")
    with open("./templates/printing_metres.jinja", "r", encoding="utf-8") as f:
        with open("./static/assets/logobalta.jpg", "rb") as img:
            imgb64 = base64.b64encode(img.read()).decode("utf-8")
        t = Template(f.read())
        pdf_name = "./stock/" + datetime.strftime(datetime.now(), "%Y_%m_%d__%H_%M_%S_- KVADRATURA.pdf")
        pdfkit.from_string(t.render(
            report_timestamp=str(datetime.strftime(datetime.now(),'%d.%m.%Y-%H:%M:%S')),
sardes=sardes, gaspara=gaspara, allures=allures, erva=erva, rivenna=rivenna, s=s, company_logo=imgb64), pdf_name)
    if s>0:
        return send_file(pdf_name, as_attachment=True)
    else: 
        return redirect("/search?error=something")

@admin.post("/change")
def update_post():
    kolekcija = request.form.get("kolekcija")
    sifra = request.form.get("sifra")
    D80x150 = int(request.form.get("D80x150"))
    D80x300  = int(request.form.get("D80x300"))
    D120x200  = int(request.form.get("D120x200"))
    D160x230  = int(request.form.get("D160x230"))
    D200x300 = int(request.form.get("D200x300"))
    D120x120  = int(request.form.get("D120x120"))
    D160x160  = int(request.form.get("D160x160"))
    D200x200 = int(request.form.get("D200x200"))
    kvadratura =  D80x150 * 1.2 +  D80x300 * 2.4 + D120x200 * 2.4 + D160x230 * 3.76 + D200x300 * 6 + D120x120 * 1.44 + D160x160 * 2.56 + D200x200 * 4
    kvadratura = round(kvadratura, 2)
    is_saved_tepisi = l_login.save(kolekcija, sifra, D80x150, D80x300, D120x200, D160x230, D200x300, kvadratura, D120x120, D160x160, D200x200)
    print(is_saved_tepisi)
    if is_saved_tepisi>0:
        return redirect("/index_stock?success=update")
    else:
        return redirect("/?error=tepih_saving")    
    
@admin.get("/saldo")
def saldo_m():
    b = l_login.saldo_metres()
    sardes = 0
    gaspara = 0
    allures = 0
    rivenna = 0
    erva = 0
    s = 0
    for a in b:
        if a[0] == "Sardes":
             sardes += float(a[8])
        elif a[0] == "Gaspara":
            gaspara += float(a[8])
        elif a[0] == "Allures":
            allures += float(a[8])
        elif a[0] == "Erva":
            erva += float(a[8])
        elif a[0] == "Rivenna":
            rivenna += float(a[8])
    sardes = round(sardes, 2)
    gaspara = round(gaspara, 2)
    allures = round(allures, 2)
    erva = round(erva, 2)
    rivenna = round(rivenna, 2)
    s = sardes + gaspara + allures + erva + rivenna
    s = round(s,2)
    gl.GlobalComponents.set("sardes", sardes)
    gl.GlobalComponents.set("gaspara", gaspara)
    gl.GlobalComponents.set("allures", allures)
    gl.GlobalComponents.set("rivenna", rivenna)
    gl.GlobalComponents.set("erva", erva)
    gl.GlobalComponents.set("s", s)
    return render_template("saldo.jinja", sardes=sardes, gaspara=gaspara, allures=allures, erva=erva, rivenna=rivenna, s=s)

@admin.get("/izvestaji")
def izvestaji():
    error = None 
    success = None 
    error_key = request.args.get("error", None)
    success_key =  request.args.get("success", None)
    if error_key is not None:
        error = el.ErrorList.get(error_key)
    if success_key is not None:
        success = sl.SuccessList.get(success_key)
    return render_template("/izvestaji.jinja",
                           error=error, success=success)

@admin.post("/izvestaji")
def login_submission():
    try:
        user_data = request.form["glavna_sifra"]
        if user_data =="AtijaMaida2022.":
            return redirect("/dnevni_izvestaji?success=login_success")
        else:
            return redirect("/izvestaji?error=invalid_password")
    except:
        return redirect("/izvestaji?error=vec_ste_ulogovani")
    
    
@admin.get("/dnevni_izvestaji")
def dnevni_izvestaji():
    error = None 
    success = None 
    error_key = request.args.get("error", None)
    success_key =  request.args.get("success", None)
    if error_key is not None:
        error = el.ErrorList.get(error_key)
    if success_key is not None:
        success = sl.SuccessList.get(success_key)
    dan = datetime.now()
    datum = dan.strftime("%d.%m.%Y")
    sve = l_login.find_saldo()
    s = 0
    for i in sve:
        s += float(i[1])
    return render_template("/dnevni_izvestaji.jinja",
                           error=error, success=success, datum=datum, sve=sve, s=s)
    
@admin.post("/dnevni_izvestaji")
def dnevni_izvestaji_post():
     s = 0
     unos = request.form["cena"]
     dan = request.form["datum"]
     sacuvano = l_login.save_saldo(dan, unos)
     return redirect("/dnevni_izvestaji?success=uspesno")