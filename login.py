from flask import Blueprint, render_template, request, session, redirect, flash
import protect
from mongo import db

login = Blueprint("login", __name__, template_folder="templates", static_folder="static")

@login.route("/login/", methods=['GET', 'POST'])
def _login():
    if "login" in session:
        return redirect("/dashboard/")
    
    if request.method == "POST":
        email = request.form['email']
        password = protect.protect(request.form['password'])
        check = db.members.find_one({"email":email, "password":password})
        if check:
            session['login'] = username
            if request.form.get("remember"):
                session.permanent = True
            return redirect("/dashboard/")
        else:
            flash("Login Failed")
        
    return render_template("login.html")