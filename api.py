#This API is for the chat stuff

from mongo import db
from flask import Flask, Blueprint, redirect, render_template
from bson import ObjectId
import time

api = Blueprint(__name__, "api")

@api.route("/api/get/")
def get():
    chat = db.chat.find().sort("_id", 1)
    if chat.count() >= 100:
        data = db.chat.find().sort("_id", -1)
        for x in data:
            break
        db.chat.remove(x)

    return render_template("api_get.html", chat=chat)


@api.route("/api/send/<key>/<message>")
def send(key, message):
    check = check(key)
    if check:
        db.chat.insert({"from":check['username'], "message":message, "time":time.time()})


def check(key):
    check = db.members.find_one({"_id":ObjectId(key)})
    if not check:
        return False
    else:
        return check
