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
    return render_template("dashboard.html", admin=check['admin'])

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
    return render_template("edit.html", user=check, admin=check['admin'])

@account.route("/account/games", methods=['GET','POST'])
def deposit_():
    check = wallet.check()
    if not check:
        return redirect("/")
    
    games = db.games.find({"rsname":check['rsname']}).sort("_id", -1)
    
    return render_template("games.html", games=games, admin=check['admin'])
    
@account.route("/account/games/delete/<uid>",methods=['GET','POST'])
def delete_(uid):
	user = wallet.check()
	user = db.members.find_one({"email":session['login']})
	check = db.games.find_one({"creator":user['rsname']})
	
	if check or user['admin']:
		if db.games.remove({"id":uid}):
			return redirect("/account/games")
		else:
			return "This game does not exist. <a href='javascript:history.back()'>Click</a> here to go back."
	else:
		return "Shame on you. This game does not belong to you."
