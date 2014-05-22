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

@admin.route("/admin/bank")
def bank_():
	#user = wallet.check()
	#if not user or not user['admin']:
	#	return redirect("/")
	return render_template("bank.html")
