from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.host_model import Host

# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)

# === 1. Remeber to import file on server.py 
# === Note: Controllers pull in classes




@app.route('/host_settings')
def host_settings():
    #set this info
    session["host"] = data = {}
    data = { "id": session['id'] }
    host_info = Host.get_host_info(data)
    return render_template('host_settings.html', host_info=host_info)

#finish this route
@app.route('/new_host_info')
def new_host_info():
    if not User.validate_user(request.form):
            session["host"] = data