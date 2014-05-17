from flask import Blueprint, render_template, flash, redirect, request, session
from mongo import db

create = Blueprint(__name__, "create")

@create.route("/create/", methods=['GET', 'POST'])
def create_():
    return render_template("create.html")