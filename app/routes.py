# app/routes.py

from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, bcrypt 
from .models import User, Message
from flask import current_app as app
from flask import jsonify
from flask_login import login_required, current_user, login_user, logout_user
from .utils import set_user_online, set_user_offline, update_last_active, get_online_users



@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return redirect(url_for('chat'))
        else:
            flash('Username already exists.')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            login_user(user)
            user.is_active = True
            user.is_online = True
            return redirect(url_for('chats'))
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        receiver_username = request.form['receiver']
        content = request.form['content']
        
        receiver = User.query.filter_by(username=receiver_username).first()
        if receiver:
            new_message = Message(content=content, sender_id=user.id, receiver_id=receiver.id)
            db.session.add(new_message)
            db.session.commit()
        else:
            flash('User not found.')
    
    messages_sent = user.messages_sent
    messages_received = user.messages_received
    return render_template('chat.html', messages_sent=messages_sent, messages_received=messages_received, user=user)


################################### testing code ##################################################

@app.route('/chats', methods=['GET', 'POST'])
@login_required
def chats():
    if 'user_id' not in session:
        app.logger.debug('User ID not in session. Redirecting to login.')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    app.logger.debug(f'Current User: {user}')

    if request.method == 'POST':
        receiver_username = request.form['receiver']
        content = request.form['content']
        app.logger.debug(f'Sending message to: {receiver_username} with content: {content}')

        receiver = User.query.filter_by(username=receiver_username).first()
        if receiver:
            new_message = Message(content=content, sender_id=user.id, receiver_id=receiver.id)
            db.session.add(new_message)
            db.session.commit()
        else:
            flash('User not found.')
            app.logger.debug('User not found.')

    messages_sent = user.messages_sent
    messages_received = user.messages_received
    active_users = get_online_users()

    app.logger.debug(f'Messages Sent: {messages_sent}')
    app.logger.debug(f'Messages Received: {messages_received}')
    app.logger.debug(f'Active Users: {active_users}')

    return render_template('chat.html', messages_sent=messages_sent, messages_received=messages_received, user=user, active_users=active_users)



######################################################################################################








@app.before_request
def before_request():
    if current_user.is_authenticated:
        # Update last active before every request
        update_last_active(current_user.id)



# @app.route('/active_users')
# def active_users():
#     app.logger.debug("Fetching active users")
#     active_users = User.query.filter_by(is_online=True).all()
#     return jsonify([user.to_dict() for user in active_users])


@app.route('/active_users')
def active_users():
    app.logger.debug("Fetching active users")
    active_users = User.query.filter_by(is_online=True, is_active=True).all()
    
    # Convert the list of User objects to a list of dictionaries
    users_list = [{'username': user.username} for user in active_users]
    # Return the list of active users as JSON
    return jsonify(users_list)


@app.route('/inactive_users')
def inactive_users():
    app.logger.debug("Fetching inactive users")
    # Fetch users who are not online and are marked inactive
    users = User.query.filter_by(is_online=False).all()
    user_list = [{'username': user.username} for user in users]
    return jsonify(user_list)




@app.route('/logout')
def logout():
    # logout_user()
    user = User.query.get(session['user_id'])
    if user:
        user.is_online = False
        # user.is_active = False
        db.session.commit()
    session.pop('user_id', None)
    return redirect(url_for('login'))
# @app.route('/logout')
# def logout():
#     user_id = session.get('user_id')
#     if user_id:
#         user = User.query.get(user_id)
#         if user:
#             app.logger.debug(f'Logging out user: {user.username}, setting is_online to False')
#             user.is_online = False  # Set user as offline
#             db.session.commit()
#             session.pop('user_id', None)  # Remove user ID from session
    return redirect(url_for('login'))