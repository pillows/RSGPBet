from flask import Blueprint, render_template, flash, redirect, request, session
from mongo import db

wallet = Blueprint(__name__, "wallet")

@wallet.route("/wallet/", methods=['GET', 'POST'])
def wallet_():
    return render_template("wallet.html")

@wallet.route("/wallet/withdraw", methods=['GET','POST'])
def withdraw_():
    return render_template("withdraw.html")

@wallet.route("/wallet/deposit", methods=['GET','POST'])
def deposit_():
    return render_template("deposit.html")
    
@wallet.route("/wallet/transfer", methods=['GET','POST'])
def transfer_():
    return render_template("transfer.html")