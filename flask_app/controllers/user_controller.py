from ast import MatchSequence
from nis import match
from flask_app import app
from flask import render_template,redirect,request,session,flash

from flask_app.models.user_model import User
from flask_app.models.address_model import Address
from flask_app.models.message_model import Message
from flask_app.models.flock_model import Flock
from flask_app.models.flock_user_model import Flock_User
from flask_app.models.host_model import Host


from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# === 1. Remeber to import file on server.py 
# === Note: Controllers pull in classes

# ==========================================
# ROUTE: home page
# ==========================================
@app.route('/')
def index():
    ip_addr = request.remote_addr
    session["ip"] = ip_addr

    if 'id' in session:
        return redirect('/dashboard')
    elif not "counter" in session:
        session["counter"] = 10

    if session["counter"] == 1:
        return redirect("/lock")
    else:
        if 'form' not in session: 
            session["form"] = data = {"first_name": "", "last_name": "", "phone": "","email": "","gender":"", "password": "", "confirm_password": ""}
        return render_template('index.html')

# ========================================
# ROUTE: to dashboard if logged in : go to home (/)
# ========================================
@app.route('/dashboard')
def render_dashboard():
    if session["counter"] == 1:
        return redirect("/lock")
    else:
        if 'id' in session:
            data = { "id": session['id'] }
            user_info = User.get_user_info(data)
            all_flocks = Flock.select_all_flocks(data)
            flock_info = Flock.get_admin_info(data)
            host_info = Host.get_host_info(data)
            # all_messages = Message.get_all_for_message(data)
            return render_template('dashboard.html',user_info=user_info,all_flocks=all_flocks,flock_info=flock_info,host_info=host_info)
        else:
            flash("Please Loin","info")
            return redirect('/')

# ========================================
# ROUTE: user settings page
# ========================================
@app.route('/user_settings')
def user_settings():
    data = { "id": session['id'] }
    user_info = User.get_user_info(data)
    user_admin = Flock.get_user_admin(data)
    return render_template('user-settings.html',user_info=user_info,user_admin=user_admin)

# ========================================
# ROUTE: lock
# ========================================
@app.route('/lock')
def lock():
    # session["counter"] = 10
    # return render_template('index.html')
    return render_template('lock.html')

# ==========================================
# INSERT: add new user
# ==========================================
@app.route('/new_user', methods=["POST"])
def new_user():
    if session["counter"] == 1:
        return redirect("/lock")
    else:
        data = {
            "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'],
            "phone" : request.form['phone'],
            "email" : request.form['email'],
            "password" : request.form['password'],
            "confirm_password" : request.form['confirm_password']
        }

        if not User.validate_user(request.form):
            session["form"] = data
            return redirect('/')
        else:
            data["password"] = bcrypt.generate_password_hash(request.form['password'])

            new_user_id = User.create_new_user(data)
            session['id'] = new_user_id
            return redirect('/dashboard')

# ========================================
# INSERT: user to group
# ========================================
@app.route('/accept_user',methods=["POST"])
def accept_user():
    mess_id = request.form['mess_id']
    from_id = request.form['from_id']
    welcome_message = "Welcome to the " +  request.form['flock_title'] + "!"

    data = {
        "user_id" : from_id,
        "flock_id": request.form['flock_id']
    }
    Flock_User.add_user_to_flock(data)
    dataMessage = {
        "message" : welcome_message,
        "message_type" : "welcome",
        "from_id" : session['id'],
        "flock_id": request.form['flock_id']
    }
    welcome_id = Message.save_message(dataMessage)

    dataTwo = {
        "user_id" : request.form['from_id'],
        "message_id" : welcome_id
    }

    Message.save_to_from_info(dataTwo)

    #delet the old mesaage info
    dataThree = {
        "id" : request.form['mess_id'],
        "user_id" : session['id']
    }
    
    Message.delete_message(dataThree)
    Message.delete_user_message(dataThree)

    return redirect("/messages")

# ========================================
# UPDATE: user settings
# ========================================
@app.route('/update_user_settings',methods=["POST"])
def update_user_settings():
    data = {
        "id": request.form["id"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "phone": request.form["phone"],
        "email": request.form["email"]
    }

    if not User.validate_update_user(request.form):
        return redirect ('/user_settings')
    else:
        flash('Settings have been updated',"info")
        User.update_user_info(data)
        return redirect('/dashboard')

# ========================================
# UPDATE: address
# ========================================
@app.route('/update_address',methods=["POST"])
def update_address():
    data = {
        "address": request.form["address"],
        "city": request.form["city"],
        "state": request.form["state"],
        "zip": request.form["zip"],
        "user_id": request.form["user_id"]
    }
    
    dataTwo = {
        "user_id": request.form["user_id"]
    }
    user_has_address = Address.has_address(dataTwo)

    if not Address.validate_update_address(request.form): 
        return redirect ('/user_settings')
    elif user_has_address == "0":
        flash("Address has been addded to your account","info")
        Address.add_address(data)
    else:
        flash("User info has been updated!","info")
        Address.update_address(data)
    return redirect ('/dashboard')

# ========================================
# UPDATE: password
# ========================================
@app.route('/update_password', methods=["POST"])
def update_password():
    data = {
        "password": request.form['password'],
        "id": request.form['id']
    }
    password_in_db = User.get_by_password(data)

    if not User.validate_password(request.form):
        return redirect('/user_settings')
    elif not bcrypt.check_password_hash(password_in_db.password, request.form['old_password']):
        flash("Old password doesn't match what we have in the system","password")
        return redirect('/user_settings')
    else:
        flash("Password has been updated!","info")
        return redirect('/dashboard')

# ========================================
# VALIDATION: Login
# ========================================
@app.route('/user_login',methods=["POST"])
def user_login():
    if session["counter"] == 1:
        return redirect("/lock")
    else:
        data = { "email" : request.form["email"] } 
        email_in_db = User.get_by_email(data)

        if not request.form["email"]:
            session["counter"] = session["counter"] - 1
            flash(f"Invalid Email/Password {session['counter']} chance(s) left","login")
            return redirect("/")
        else:
            if email_in_db == "0":
                session["counter"] = session["counter"] - 1
                flash(f"Email does not exsist {session['counter']} chance(s) left","login")
                return redirect("/") 
            if not bcrypt.check_password_hash(email_in_db.password, request.form['password']):
                session["counter"] = session["counter"] - 1
                flash("Invalid Email/Password","login")
                return redirect('/')
                
            session['id'] = email_in_db.id
            session["counter"] = 10
            return redirect("/dashboard") 

# ========================================
# LOGOUT: clear all cookies
# ========================================
@app.route('/logout')
def logout():
    session["counter"] = 0
    if session["counter"] == 10:
        return redirect("/lock")
    else:
        session.clear()
        return redirect('/')
        
# ========================================
# DELETE: user
# ========================================
@app.route('/delete_user/<int:id>')
def delete_user(id):
    data = { "id": id }
    Address.delete_user_address(data)
    Message.delete_user_messages(data)
    User.delete_user(data)
    return redirect('/logout')