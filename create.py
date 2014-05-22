from flask import Blueprint, render_template, flash, redirect, request, session
from mongo import db
import wallet
import uuid
import random

create = Blueprint(__name__, "create")

@create.route("/create/", methods=['GET', 'POST'])
def create_():
    check = wallet.check()
    if not check:
        return redirect("/")
    if request.method == "POST":
        if not request.form.get("amount"):
            
            flash("You need to bet an amount.")
            return redirect("/create/")
        amount = request.form['amount']
        try:
            amount = int(amount)
        except:
            flash("Amount needs to be an integer.")
            return redirect("/create/")
        if amount > check['wallet']:
            flash("You don't have enough gold.")
            return redirect("/create/")
        if amount < 10000:
            flash("You have to bet atleast 10000.")
            return redirect("/create/")
        gameid = uuid.uuid4().hex
        game = request.form['radios1']
        if game != "bank":
            try:
                players = int(request.form['radios'])
            except:
                flash("Number of players has to be an integer.")
                return redirect("/create/")
            db.games.insert({"type":"Dice Duel", "creator":check['rsname'], "rsname":check['rsname'], "id":gameid, "bet":amount, "participants":1, "max_participants":players, "win":None, "roll":None, "resullt":None})
            db.members.update({"rsname":check['rsname']}, {"$set":{"wallet":check['wallet'] - amount}})
        elif game == "bank":
            db.members.update({"rsname":check['rsname']}, {"$set":{"wallet":check['wallet'] - amount}})
            roll = random.randint(1, 101)
            if roll > 60:
                win = (amount * 2)
                win -= win * 0.05
                db.games.insert({"rsname":check['rsname'], "type":"Bank", "id":gameid, "bet":amount, "participants":1, "max_participants":1, "win":amount, "roll":roll, "result":"You won!"})
                db.members.update({"rsname":check['rsname']}, {"$set":{"wallet":check['wallet'] + win}})
            
            if roll <= 60:
                db.games.insert({"rsname":check['rsname'], "type":"Bank", "id":gameid, "bet":amount, "participants":1, "max_participants":1, "win":0, "roll":roll, "result":"You lost"})
            
        flash("Game has been created.")
        return redirect("/create/")
    return render_template("create.html", admin=check['admin'])
