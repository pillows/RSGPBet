from flask import Blueprint, render_template, request, session, redirect
from mongo import db
import api

index = Blueprint("index", __name__, template_folder="templates", static_folder="static")

@index.route("/", methods=['GET', 'POST'])
def _index():
    if "login" in session:
        check = db.members.find_one({"email":session['login']})
    else:
        check = None
    bank = db.games.find({"type":"Bank"}).sort("_id", -1).limit(3)
    dd = db.games.find({"type":"Dice Duel"}).sort("_id", -1).limit(3)
    return render_template("index.html", user=check, dd=dd, bank=bank)
