"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, jsonify, send_file, send_from_directory, flash, url_for, redirect, session, abort
import os
import json
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from app.models import Posts, Likes, Follows, Users
from flask_login import login_user, logout_user, current_user, login_required
# from app.forms import
import jwt

###
# Routing for your application.
###
# def requires_auth(t):
#   @wraps(t)
#   def decorated(*args, **kwargs):
#     auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)
#     if not auth:
#         return jsonify({'error': "Access Denied: No Token Found"}), 401
#     else:
#         try:
#             userdata = jwt.decode(auth.splt(" ")[1], app.cofig['SECRET_KEY'])
#             user= Users.query.filter_by(username= userdata['user']).first
#             #modify that
#             if user is None:
#                 return jsonify({'error': "Access Denied: No User Found"}), 401
            
#         except jwt.exceptions.InvalidSignatureError as e:
#             return jsonify({'error': "Access Denied: Invalid Token"}), 401
#         except jwt.exceptions.DecodeError as e:
#             return jsonify({'error': "Access Denied: Invalid Token"}), 401
#         return t(*args, **kwargs)
#   return decorated

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None) 

    
        if not auth:
            return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
        elif len(parts) == 1:
            return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
        elif len(parts) > 2:
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

        token = parts[1]
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
        except jwt.DecodeError:
            return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

        g.current_user = user = payload
        return f(*args, **kwargs)

    return decorated


@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/csrf-token',methods=["GET"])
def getcsrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('api/v1/register', methods=['POST'])
def register():
    #form = 
    if request.method=="POST":
        if form.validate_on_request:
            try:
                username = form.username.data
                password = form.password.data
                firstname = form.firstname.data
                lastname = form.lastname.data
                email  = form.email.data
                location = form.location.data
                biography = form.biography.data
                profile_photo = form.profile_photo.data
                # joined_on = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                filename= secure_filename(profile_photo.filename)
                profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if isAPhoto(filename):
                    user= Users(username=username, password= password, firstname= firstname, lastname = lastname, email = email, location =  location, biography = biography, profile_photo = filename)
                    db.session.add(user)
                    db.session.commit()
                    flash("You have registered sucessfully!","success")
                    return jsonify(message="User created successfully"), 201
            #username, password, firstname, lastname, email, location, biography, profile_photo
                else:
                    flash("The file you uploaded is not a photo","error")
            except Exception as e:
                db.session.rollback()
                return jsonify(message="Error creating user: " + str(e))
    return jsonify(errors=form_errors(form))


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    # form = LoginForm()
    if request.method=="POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            timestamp= datetime.utcnow()
            user = Users.query.filter_by(username=username).first()
            if user is not None and user.check_password_hash(user.password, password):
                # session['userid'] = user.id
                payload = {'sub': user.email, "iat":timestamp, "exp": timestamp + timedelta(minutes = 30)}
                token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm = 'HS256')
                return jsonify(message = 'User successfully logged in.', token=token)
            return jsonify(errors="Invalid username or password")
        return jsonify(errors=form_errors(form))
    return jsonify(errors=form_errors(form))

@app.route('/api/auth/logout', methods = ['GET'])
@requires_auth
@login_required
def logout():
    logout_user()
    session.clear()
    return jsonify(message = "User sucessfully logged out.")

@app.route('/api/v1/users/<user_id>/posts', methods=['POST'])
@requires_auth
@login_required
def createPost(user_id):
    #form = CreatePost()
    if request.method=="POST":
        if form.validate_on_submit():
            photo = form.photo.data
            caption = form.description.data
            #created_on = datetime.utcnow()
            filename = secure_filename(photo.filename)
            try:
                post= Posts(caption=caption, photo = filename, user_id= user_id)
                db.session.add(post)
                db.session.commit()
                return jsonify(message="Successfully created a new post"), 201
            except Exception as e:
                db.session.rollback()
                return jsonify(errors = f"Error creating post: {e}")
        else:
            return jsonify(errors=form_errors(form))
    return jsonify(errors=form_errors(form))


@app.route('/api/v1/users/<user_id>/posts', methods=['GET'])
@login_required
@requires_auth
def getUserPost(user_id):
    if request.method=="GET":
            temp = Posts.query.filter_by(user_id=user_id).all()
            posts= []
            for post in temp:
                p={"id":post.id, "user_id": post.user_id, "photo": post.photo,"description": post.caption, "created_on":post.created_on }
                posts.append(p)
            return jsonify(posts= posts)
    return jsonify(errors=form_errors(form))

@app.route('/api/users/<user_id>/follow', methods=['POST'])
@login_required
@requires_auth
def follow(user_id):
    if request.method=="POST":
            if current_user.id != user_id:
                try:
                    follower= current_user.id
                    followee = Users.query.filter_by(id=user_id).first()
                    if followee:
                        follow = Follows(follower_id=follower, user_id = user_id)
                        db.session.add(follow)
                        db.session.commit()
                        return jsonify(message="You are now following that user."), 201
                    else:
                        return jsonify(message="User not found."), 404
                except Exception as e:
                    db.session.rollback()
                    return jsonify(errors = f"Internal Error: {e}")
            else:
                return jsonify(errors = f"You can't follow yourself.")
    else:
        return jsonify(errors=form_errors(form))

@app.route('/api/v1/posts', methods=['GET'])
@login_required
@requires_auth
def getPosts():
    if request.method=="GET":
        allPosts = Posts.query.all()
        posts= []
        for post in allPosts:
            id=post.id
            likes= Likes.query.filter_by(post_id = id).count()
            p={"id":id, "user_id": post.user_id, "photo": post.photo,"caption": post.caption, "created_on":post.created_on,"likes":likes}
            posts.append(p)
        return jsonify(posts= posts)
    return jsonify(errors=form_errors(form))


@app.route('/api/v1/posts/<post_id>/like', methods=['POST'])
@login_required
@requires_auth
def likePost(post_id):
    if request.method=="POST":
        likes= Likes.query.filter_by(post_id = post_id, user_id=current_user.id).count()
        if likes == 0:
            like = Likes(post_id=post_id, user_id=current_user.id)
            totallikes= Likes.query.filter_by(post_id = post_id).count()
            db.session.add(like)
            db.session.commit()
            return jsonify(message="Post liked!", likes=totallikes)
        else:
            Likes.query.filter_by(post_id = post_id, user_id=current_user.id).delete()
            totallikes= Likes.query.filter_by(post_id = post_id).count()
            db.session.commit()
            return jsonify(message="You removed your like from this post.", likes=totallikes)
    return jsonify(errors=form_errors(form))
            

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

def isAPhoto(filename):
#Checks if a file is a photo
# if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpg"):
    return filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg') or filename.lower().endswith('.png') or filename.lower().endswith('.gif')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
