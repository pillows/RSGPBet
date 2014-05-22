from flask import Blueprint, render_template, request, session, redirect
from mongo import db
import api

index = Blueprint("index", __name__, template_folder="templates", static_folder="static")

@index.route("/", methods=['GET', 'POST'])
def _index():
    if "login" in session:
        check = db.members.find_one({"email":session['login']})
        admin = check['admin']
    else:
        admin = None
        check = None
    bank = db.games.find({"type":"Dice Duel", "result":{"$ne":None}}).sort("_id", -1).limit(20)
    dd = db.games.find({"type":"Dice Duel", "result":None}).sort("_id", -1).limit(20)
    return render_template("index.html", user=check, dd=dd, bank=bank, admin=admin)
