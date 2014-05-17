from flask import Blueprint, render_template, flash, redirect, request, session
from mongo import db

account = Blueprint(__name__, "account")

@account.route("/account/", methods=['GET', 'POST'])
def account_():
    return render_template("dashboard.html")

@account.route("/account/edit", methods=['GET','POST'])
def withdraw_():
    return render_template("edit.html")

@account.route("/account/games", methods=['GET','POST'])
def deposit_():
    return render_template("games.html")