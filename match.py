from flask import Blueprint, render_template, flash, redirect, request, session
from mongo import db
import wallet
from bson import ObjectId
import random

match = Blueprint(__name__, "account")

@match.route("/match/<uid>", methods=['GET', 'POST'])
def match_(uid):
    user = wallet.check()
    if not user:
        return redirect("/")
    
    if request.method == "POST":
        check = db.games.find_one({"rsname":user['rsname'], "id":uid})
        if check:
            flash("You are already in this game.")
            return reirect("/match/"+uid)

        c2 = db.games.find_one({"id":uid})
        if c2['participants'] >= c2['max_participants']:
            flash("There are too many people in this game.")
            return redirect("/match/"+uid)
        
        if user['wallet'] < c2['bet']:
            flash("You don't have enough gold to bet.")
            return redirect("/match/"+uid)

        c3 = db.games.find({"id":uid})
        control = None
        for x in c3:
            participants = x['participants'] + 1
            db.games.update({"_id":ObjectId(x['_id'])}, {"$set":{"participants":x['participants']+1}})
            control = x

        db.games.insert({"type":"Dice Duel", "creator":control['creator'], "rsname":user['rsname'], "id":control['id'], "bet":control['bet'], "participants":control['participants']+1, "max_participants":control['max_participants'], "win":None, "roll":None, "resullt":None})
        db.members.update({"rsname":user['rsname']}, {"$set":{"wallet":user['wallet'] - control['bet']}})
        if control['max_participants'] == control['participants'] + 1:
    
            
            people = db.games.find({"id":uid}) 
            for x in people:
                while True:
                    roll = random.randint(1, 101)
                    if db.games.find_one({"id":uid, "roll":roll}):
                        pass
                    else:
                        db.games.update({"id":uid, "rsname":x['rsname']}, {"$set":{"roll":roll}})
                        break
            winner = {"roll":-5}
            check_winner = db.games.find({"id":uid})
            for x in check_winner:
                if x['roll'] > winner['roll']:
                    winner = x
            
            
            member = db.members.find_one({"rsname":winner['rsname']}) 
            final_update = db.games.find({"id":uid})
            for x in final_update:
                if x['rsname'] == winner['rsname']:
                    db.games.update({"rsname":x['rsname'], "id":uid}, {"$set":{"win":control['bet'] * x['participants'] - 1, "result":winner['rsname']+" Wins!"}})
                    db.members.update({"rsname":winner['rsname']}, {"$set":{"wallet":member['wallet'] + control['bet'] * x['participants']}})
                else:
                    db.games.update({"rsname":x['rsname'], "id":uid}, {"$set":{"win":0, "result":winner['rsname']+" Wins!"}})

            return redirect("/match/"+uid)

    out = []
    data = db.games.find({"id":uid}).sort("_id", -1)
    for x in data:
        out.append(x)
    control = out[0]
    return render_template("match.html", games=out, control = x, admin=user['admin'])
