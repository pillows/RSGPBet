from flask import Blueprint, render_template, flash, redirect, request, session
from mongo import db
import wallet
from bson import ObjectId

admin = Blueprint(__name__, "account")

@admin.route("/admin/tickets", methods=['GET', 'POST'])
def tickets_():
    user = wallet.check()
    if not user or not user['admin']:
        return redirect("/")
    tickets = db.tickets.find({"status":"Not Completed"}).sort("_id", 1)
    return render_template("tickets.html", tickets=tickets)
	
@admin.route("/admin/tickets/complete/<oid>")
def complete(oid):
    user = wallet.check()
    if not user or not user['admin']:
        return redirect("/")
    db.tickets.update({"_id":ObjectId(oid)}, {"$set":{"status":"Transaction Complete"}})
    return redirect("/admin/tickets")

@admin.route("/admin/tickets/deny/<oid>")
def deny(oid):
    user = wallet.check()
    if not user or not user['admin']:
        return redirect("/")
    db.tickets.update({"_id":ObjectId(oid)}, {"$set":{"status":"Transaction could not be completed, try making another request."}})
    return redirect("/admin/tickets")

@admin.route("/admin/tickets/<uid>")
def tickets_view(uid):
    user = wallet.check()
    if not user or not user['admin']:
        return redirect("/")
	return render_template("tickets_view.html")

@admin.route("/admin/bank", methods=['GET', 'POST'])
def bank_():
    user = wallet.check()
    if not user or not user['admin']:
	    return redirect("/")

    total = db.bank.find_one()
    if not total:
        db.bank.insert({"total":0})
        total = db.bank.find_one()
    
    if request.method == "POST":
        if request.form.get("withdraw"):
            name = request.form['rsname']
            deposit = request.form['finalwithdraw']
            try:
                deposit = int(deposit)
            except:
                flash("Deposit must be an integer.")
                return redirect("/admin/bank")

            check = db.members.find_one({"rsname":name})
            if not check:
                flash("RSname does not exist on our site.")
                return redirect("/admin/bank")
            
            db.members.update({"rsname":name}, {"$set":{"wallet":check['wallet'] - deposit}})
            db.bank.update({"total":total['total']}, {"$set":{"total":total['total'] - deposit }})
            flash("Withdraw successful")
            return redirect("/admin/bank")
        if request.form.get("deposit"):
            name = request.form['rsname']
            deposit = request.form['finaldeposit']
            try:
                deposit = int(deposit)
            except:
                flash("Deposit must be an integer.")
                return redirect("/admin/bank")

            check = db.members.find_one({"rsname":name})
            if not check:
                flash("RSname does not exist on our site.")
                return redirect("/admin/bank")
            
            db.members.update({"rsname":name}, {"$set":{"wallet":check['wallet'] + deposit}})
            db.bank.update({"total":total['total']}, {"$set":{"total":total['total'] + deposit }})
            flash("Deposit successful")
            return redirect("/admin/bank")
    return render_template("bank.html", total=total)
