from flask import Blueprint, render_template, flash, redirect, request, session
from mongo import db

admin = Blueprint(__name__, "account")

@admin.route("/admin/tickets", methods=['GET', 'POST'])
def tickets_():
	return render_template("tickets.html")
	
@admin.route("/admin/tickets/<uid>")
def tickets_view(uid):
	return render_template("tickets_view.html")