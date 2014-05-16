from flask import Blueprint, render_template, flash, redirect, request, session
from mongo import db
import protect

login = Blueprint(__name__, "login")

@login.route("/login/", methods=['GET', 'POST'])
def login_():
    if "session" in session:
        return redirect("/")

    if request.method == "POST":
        email = request.form['email']
        password = protect.protect(request.form['password'])
        check = db.members.find_one({"email":email, "password":password})
        if not check:
            flash("Invalid Login")
            return redirect("/login/")
        else:
            session['login'] = email
            return redirect("/")
    return render_template("login.html")
