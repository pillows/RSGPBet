from flask import Blueprint, render_template, request, session, redirect, flash
import protect
from mongo import db
import os
import time
import uuid
import random
import re

register = Blueprint("register", __name__, template_folder="templates", static_folder="static")

@register.route("/register/", methods=['GET', 'POST'])
def _register(plan_choice=None):
    if "login" in session:
        return redirect("/dashboard/")

    if request.method == "POST":
        runescape = request.form['rsname']
        password = protect.protect(request.form['password'])
        confirm = protect.protect(request.form['confirmpassword'])
        email = request.form['email']
        
        check = re.findall("^[+a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$", email)
        if not check:
            flash("You need to enter a valid email.")
            return redirect("/register/")
        if not request.form['password'] or not name or not email:
            flash("You must fill out all the fields.")
            return rendirect("/register/")
        if password != confirm:
            flash("Passwords did not match")
        elif db.members.find_one({"email":email}):
            flash("Email already taken")
        else:
            db.members.insert({"name":name, "password":password, "email":email, "rsname":runescape, "wallet":0})
            session['login'] = email
            return redirect("/dashboard/")
            

            #Plans: 1 - Free 10mb; 2 - $10 500mb; 3 - $15 1GB; 4 - $20 2GB; 5 - $50 5GB; 6 - $100 10gb 
            #If timestamp=0 then plan is free
            
            ###Stripe Block Code###

            ###End Block Code###

    return render_template("register.html")
