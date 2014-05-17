from flask import Blueprint, render_template, flash, redirect, request, session
from mongo import db
import wallet

create = Blueprint(__name__, "create")

@create.route("/create/", methods=['GET', 'POST'])
def create_():
    check = wallet.check()
    if not check:
        return redirect("/")
    if request.method == "POST":
        if request.form.get("dd"):
            players = int(request.form['radios'])
        elif request.form.get("bank"):
            pass
    return render_template("create.html")
