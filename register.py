
from flask import flash, Blueprint, render_template, session, request, redirect
from mongo import db
import protect

register = Blueprint(__name__, "register")

@register.route("/register/", methods=['GET', 'POST'])
def register_():
    if "login" in session:
        return redirect("/")
    
    if request.method == "POST":
        email = request.form['email']
        password = protect.protect(request.form['password'])
        confirm = protect.protect(request.form['confirmpassword'])
        rsname = request.form['rsname']
        check = db.members.find_one({"email":email})
        if check:
            flash("Email already taken.")
            return redirect("/register/")
        elif db.members.find_one({"rsname":rsname}):
            flash("Runescape name already taken.")
            return redirect("/register/")
        elif password != confirm:
            flash("Passwords do not match.")
            return redirect("/register/")
        else:
            db.members.insert({"email":email, "password":password, "rsname":rsname, "wallet":0, "admin":False, "verified":False})
            session['login'] = email
            return redirect("/")

    return render_template("register.html")
