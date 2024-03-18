from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.flock_model import Flock
from flask_app.models.user_model import User
from flask_app.models.host_model import Host


# =============================================  
# ROUTE:  group dashboard
# =============================================  
@app.route('/flocks_dashboard/<int:flock_id>')
def flock_dashboard(flock_id):
    data = {
        "flock_id": flock_id,
        "id": session['id']
    }
    flock_info = Flock.get_flock_info(data)
    return render_template('flock_dashboard.html',flock_info=flock_info)

# =============================================  
# ROUTE: join a flock
# =============================================  
@app.route('/join_flock')
def join_flock():
    data = {
        "id": session['id']
    }
    user_info = User.get_user_info(data)
    all_flocks = Flock.select_all_flocks(data)
    return render_template("join_flock.html",user_info=user_info,all_flocks=all_flocks)

# =============================================  
# ROUTE: create a flock
# =============================================  
@app.route('/create_flock')
def create_flock():
    return render_template('create_flock.html')

# =============================================  
# ROUTE: create a flock
# ============================================= 
@app.route('/new_flock_made')
def new_flock_made():
    flash("Congrats, you've made a new flock! Happy reading","info")
    return render_template('flock_dashboard.html')

# ROUTE: flock settings
@app.route('/flock_settings/<int:flock_id>')
def flock_settings(flock_id):
    data = { "id" : flock_id }
    flock_info = Flock.get_flock_admin_info(data)
    all_memebers = User.all_flock_users(data)
    return render_template('flock_settings.html', all_memebers=all_memebers,flock_info=flock_info)

# =============================================  
# CREATE: a group
# =============================================  
@app.route('/create_new_flock',methods=["POST"])
def create_new_flock():
    data = {
        "title": request.form['title'],
        "city": request.form['city'],
        "state": request.form['state'],
        "privacy_setting": request.form['privacy_setting']
    }

    unqiue_name = Flock.unique_flock_name(data)

    if not Flock.validate_flock(request.form):
        session["group_form"] = data
        return redirect('/create_flock')
    elif len(unqiue_name):
        flash("Please pick a unique group name", "flocks")
        return redirect('/create_flock')
    else:
        new_flock_id = Flock.save_flock(data)
        dataTwo = {
            "flock_id": new_flock_id,
            "user_id": session['id']
        }

        Flock.make_creator_admin(dataTwo)
        return redirect('/new_flock_made')

# =============================================  
# UPDATE : new admin
# =============================================  
@app.route('/set_new_admin',methods=["POST"])
def set_new_admin():
    data = {
        "user_id":request.form['new_admin_id'],
        "old_admin_id":request.form['old_admin_id'],
        "flock_id":request.form['flock_id'],
        "type" : "admin"
    }
    if not Flock.validate_new_admin(request.form):
        return redirect(f"flock_settings/{data.flock_id}")
    else:
        Flock.remove_old_admin(data)
        Flock.make_new_admin(data)
        return redirect('/new_admin')

@app.route('/new_admin')
def new_admin():
    flash("You are no longer admin! Thanks for all you did","info")
    return redirect('/dashboard')

# =============================================  
# UPDATE : set new host(s)
# ============================================= 
@app.route('/set_host',methods=["POST"]) 
def set_host():
    data = {
        "user_id" : request.form["new_host_id"],
        "flock_id" : request.form["flock_id"],
        "event_date" : request.form["event_date"]
    }
    if not Host.validate_host(request.form):
        return redirect(f"flock_settings/{request.form['flock_id']}")
    else:
        Host.make_new_host(data)
        return redirect(f"/flocks_dashboard/{request.form['flock_id']}")
# =============================================  
# DELETE : leave group
# =============================================  
@app.route('/leave_flock', methods=["POST"])
def leave_flock():
    data = {
        "user_id": request.form['user_id'],
        "flock_id": request.form['flock_id']
    }
    Flock.remove_from_flock(data)
    flash("You've been remoed from the flock","info")
    return redirect('/dashboard')
