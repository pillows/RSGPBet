from flask import Flask, render_template, session, redirect
#from login import login
#from register import register
from index import index
#from dashboard import dashboard
#from settings import settings
#from support import support
#from settings import settings
#from admin_index import admin_index
#from admin_tickets import admin_tickets

app = Flask(__name__)
app.secret_key = "bpV 2Q/sF&[D`2a1Z2-85q/{1]XJRQZgWj3_q)P,=K2O9`B*RKjWiDp9P{F%WK7C"

app.debug = True
port = 5001

#app.register_blueprint(settings)
app.register_blueprint(index)
#app.register_blueprint(login)
#app.register_blueprint(register)
#app.register_blueprint(dashboard)
#app.register_blueprint(support)
#app.register_blueprint(settings)
#app.register_blueprint(admin_index)
#app.register_blueprint(admin_tickets)
#app.register_blueprint(invoice_page)

@app.route("/logout/")
def logout():
    session.pop("login")
    return redirect("/")

@app.errorhandler(404)
def four0four(e):
    return "How did you get here?", 404

if __name__ == "__main__":
    app.run(port=port)
