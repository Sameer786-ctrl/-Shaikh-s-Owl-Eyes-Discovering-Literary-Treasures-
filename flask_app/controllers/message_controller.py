from flask_app import app
from flask import render_template,redirect,request,session,flash

# from flask_app.models.user_model import User
from flask_app.models.message_model import Message
from flask_app.models.flock_model import Flock
from flask_app.models.user_model import User


# # === 1. Remeber to import file on server.py 
# # === Note: Controllers pull in classes

# ==========================================
# ROUTE: messages
# ==========================================
@app.route('/messages')
def show_all_messages():
    data = { "id": session['id'] }

    get_all_messages = Message.get_messages(data)
    return render_template('/messages.html',get_all_messages = get_all_messages)

# ============================================= 
# Route: after succesfful flock join
# ============================================= 
@app.route('/submit_request')
def request_submitted():
    return render_template('submission.html')

# ROUTE : send message

@app.route('/reply_message/<int:to_id>/<int:from_id>')
def reply_message(to_id,from_id):
    data = {
        "id":to_id
    }
    to_user_info = User.user_user_info(data)
    dataTwo = {
        "id":from_id
    }
    from_user_info = User.user_user_info(dataTwo)
    session["message"] = {"subject":"","message":"","to_id": to_id, "from_id":from_id}
    return render_template('send_message.html',to_user_info=to_user_info,from_user_info=from_user_info)
    

@app.route('/send_user_message',methods=["POST"])
def send_user_message():
    data = {
        "subject": request.form["subject"],
        "message": request.form["message"],
        "message_id": request.form["to_id"],
        "user_id": request.form["from_id"],
        "message_type": request.form["message_type"]
    }

    if not Message.validate_send_message(request.form):
        session["message"] = data
        return redirect(f"/reply_message/{request.form['to_id']}/{request.form['from_id']}")
    else:
        new_message_id = Message.save_new_message(data)
        dataTwo = {
            "message_id": new_message_id ,
            "user_id": request.form["to_id"] 
        }
        Message.save_to_from_info(dataTwo)
        return redirect('/reply_to_messages')

@app.route('/reply_to_messages')
def reply_to_messages():
    session.pop("message")
    return redirect('/messages')


# ============================================= 
# Join: Group
# ============================================= 
@app.route('/submit_join_request',methods=["POST"])
def submit_join_request():
    
    if not request.form["flock_id"]:
        flash("Please pick a flock to join!","message")
        return redirect('/dashboard')
    else:
        # save the message
        flock_id = request.form["flock_id"].split(",")[0]
        data = {
            "message" : request.form["message"],
            "message_type" : "join_request",
            "from_id" : session['id'],
            "flock_id": flock_id
        }
        new_message_id = Message.save_message(data)

        user_id = int(request.form["flock_id"].split(",")[1])

        dataTwo = {
            "user_id" : user_id,
            "message_id" : new_message_id
        }

        Message.save_to_from_info(dataTwo)
        flash("Your request to join the flock has been sent! Keep an eye on your inbox","info")
        return redirect('/dashboard')

# ============================================= 
# DELETE: message
# ============================================= 
@app.route('/delete_message/<int:mess_id>/<int:user_id>')
def delete_message(mess_id,user_id):
    data = {
        "id": mess_id,
        "user_id": user_id
    }
    Message.delete_message(data)
    Message.delete_user_message(data)
    return redirect('/messages')