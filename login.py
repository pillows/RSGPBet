<<<<<<< HEAD
from flask import Blueprint, render_template, flash, redirect, request, session
from mongo import db
import protect

login = Blueprint(__name__, "login")

@login.route("/login/", methods=['GET', 'POST'])
def login_():
    if "session" in session:
        return redirect("/")

=======
from flask import Blueprint, render_template, request, session, redirect, flash
import protect
from mongo import db

login = Blueprint("login", __name__, template_folder="templates", static_folder="static")

@login.route("/login/", methods=['GET', 'POST'])
def _login():
    if "login" in session:
        return redirect("/dashboard/")
    
>>>>>>> 4be3d0fd031b41e2bf30d3d442b05ca3c16710a6
    if request.method == "POST":
        email = request.form['email']
        password = protect.protect(request.form['password'])
        check = db.members.find_one({"email":email, "password":password})
<<<<<<< HEAD
        if not check:
            flash("Invalid Login")
            return redirect("/login/")
        else:
            session['login'] = email
            return redirect("/")
    return render_template("login.html")
=======
        if check:
            session['login'] = username
            if request.form.get("remember"):
                session.permanent = True
            return redirect("/dashboard/")
        else:
            flash("Login Failed")
        
    return render_template("login.html")
>>>>>>> 4be3d0fd031b41e2bf30d3d442b05ca3c16710a6
