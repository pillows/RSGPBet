from flask import Blueprint, render_template, flash, redirect, request, session
from mongo import db
import wallet
import protect

account = Blueprint(__name__, "account")

@account.route("/account/", methods=['GET', 'POST'])
def account_():
    check = wallet.check()
    if not check:
        return redirect("/")
    return render_template("dashboard.html")

@account.route("/account/edit", methods=['GET','POST'])
def withdraw_():
    check = wallet.check()
    if not check:
        return redirect("/")
    if request.method == "POST":
        if request.form.get("email"):
            email = request.form['email']
            check = db.members.find_one({"email":email})
            if check:
                flash("Email already exists in our database.")
                return redirect("/account/edit")
            db.members.update({"email":session['login']}, {"$set":{"email":email}})
            flash("Email updated successfully!")
            return redirect("/account/edit")
        if request.form.get("password"):
            password = protect.protect(request.form['password'])
            confirm = protect.protect(request.form['verifypassword'])
            if password != confirm:
                flash("Passwords do not match.")
                return redirect("/account/edit")
            else:
                db.members.update({"email":session['login']}, {"$set":{"password":password}})
                flash("Password updated successfully.")
                return redirect("/account/edit")
    return render_template("edit.html", user=check)

@account.route("/account/games", methods=['GET','POST'])
def deposit_():
    check = wallet.check()
    if not check:
        return redirect("/")
    
    games = db.games.find({"rsname":check['rsname']}).sort("_id", -1)
    
    return render_template("games.html", games=games)
