from flask import Blueprint, render_template, flash, redirect, request, session
from mongo import db
import wallet

admin = Blueprint(__name__, "account")

@admin.route("/admin/tickets", methods=['GET', 'POST'])
def tickets_():
    user = wallet.check()
    if not user or not user['admin']:
        return redirect("/")

	return render_template("tickets.html")
	
@admin.route("/admin/tickets/<uid>")
def tickets_view(uid):
    user = wallet.check()
    if not user or not user['admin']:
        return redirect("/")
	return render_template("tickets_view.html")
