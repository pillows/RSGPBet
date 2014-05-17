from flask import Blueprint, render_template, flash, redirect, request, session
from mongo import db

wallet = Blueprint(__name__, "wallet")

@wallet.route("/wallet/", methods=['GET', 'POST'])
def wallet_():
    user = check()
    if not user:
        return redirect("/")

    return render_template("wallet.html", user=user)

@wallet.route("/wallet/withdraw", methods=['GET','POST'])
def withdraw_():
    user = check()
    if not user:
        return redirect("/")
    if request.method == "POST":
        rsname = request.form['rsname']
        time = request.form['ticket']
        if not rsname or not time:
            flash("All fields must be filled out.")
            return redirect("/wallet/withdraw")
        db.tickets.insert({"rsname":rsname, "time":time})
        flash("Your request has been submitted.")                                                                                                                                                     
        return redirect("/wallet/withdraw")

    return render_template("withdraw.html")

@wallet.route("/wallet/deposit", methods=['GET','POST'])
def deposit_():
    user = check()
    if not user:
        return redirect("/")
    if request.method == "POST":
        rsname = request.form['rsname']
        time = request.form['ticket']
        if not rsname or not time:
            flash("All fields must be filled out.")
            return redirect("/wallet/deposit")
        db.tickets.insert({"rsname":rsname, "time":time})
        flash("Your request has been submitted.")
        return redirect("/wallet/deposit")
    return render_template("deposit.html")
    
@wallet.route("/wallet/transfer", methods=['GET','POST'])
def transfer_():
    user = check()
    if not user:
        return redirect("/")
    if request.method == "POST":
        rsname = request.form['email']
        amount = request.form['rsname']
        comment = request.form['password']
        if not rsname or not amount:
            flash("RSname and Amount must be filled out.")
            return redirect("/wallet/transfer")
        try:
            amount = int(amount)
        except:
            flash("Invalid amount")
            return redirect("/wallet/transfer")

        if user['wallet'] >= amount:
            check_ = db.members.find_one({"rsname":rsname})
            if not check_:
                flash("That user does not exist on the site.")
                return redirect("/wallet/transfer")
            else:
                db.members.update({"rsname":rsname}, {"$set":{"wallet":check_['wallet'] + amount}})
                db.members.update({"email":session['login']}, {"$set":{"wallet":user['wallet'] - amount}})
                flash("Funds transfered successfully.")
                return redirect("/wallet/transfer")
    return render_template("transfer.html")




def check():
    if "login" in session:
        return db.members.find_one({"email":session['login']})
    else:
        return False
