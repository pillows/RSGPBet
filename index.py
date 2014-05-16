from flask import Blueprint, render_template, request, session, redirect
from mongo import db
import api

index = Blueprint("index", __name__, template_folder="templates", static_folder="static")

@index.route("/", methods=['GET', 'POST'])
def _index():
    if request.method == "POST":
        message = request.form['message']
        check = db.members.find_one({"email":session['login']})
        api.send(check['_id'], message)
    return render_template("index.html")
