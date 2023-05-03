"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from functools import wraps
from app import app, db, login_manager
from app.forms import UserForm, LoginForm, PostForm
from flask import g
from flask import render_template, request, jsonify, send_file, send_from_directory, flash, url_for, redirect, session, abort
import os
import json
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from app.models import Posts, Likes, Follows, Users
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
import jwt
import psycopg2
from sqlalchemy import desc

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

ACTIVE = {}

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

@login_manager.user_loader
def load_user(id):
    user = db.session.execute(db.select(Users).filter_by(id=id)).scalar()
    if user is not None:
        ACTIVE[id] = user
    return user

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/register', methods=['POST'])
# @requires_auth
def register():
    #form = 
    if request.method=="POST":
        # if form.validate_on_request:
        try:
            user_form = UserForm()
            username = user_form.username.data
            password = user_form.password.data
            firstname= user_form.firstname.data
            lastname= user_form.lastname.data
            email = user_form.email.data
            location = user_form.location.data
            biography = user_form.biography.data
            profile_photo = request.files['profile_photo']
            
            filename=secure_filename(profile_photo.filename) #need to check if this will work when actual file is uploaded
            profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #need to check if this will work when actual file is uploaded
            if isAPhoto(filename):#need to check if this will work when actual file is uploaded
                user= Users(username=username, password= password, firstname= firstname, lastname = lastname, email = email, location =  location, biography = biography, profile_photo = filename) #need to check if this will work when actual file is uploaded
                db.session.add(user)
                db.session.commit()
                flash("You have registered sucessfully!","success")
                return jsonify(message="User created successfully"), 201
            else:
                flash("The file you uploaded is not a photo","error") #need to check if this will work when actual file is uploaded
        except Exception as e:
                db.session.rollback()
                print(e)
                return jsonify(error="Error creating user: " + str(e)), 400
    return jsonify(errors='Invalid request method'), 405


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if request.method=="POST":
        try:
            data = LoginForm()
            username = data.username.data
            password = data.password.data
            timestamp= datetime.utcnow()
            user = Users.query.filter_by(username=username).first()
            print(user)
            if user is not None and check_password_hash(user.password, password):
                payload = {'sub': user.id, "iat":timestamp, "exp": timestamp+timedelta(days=7)}
                token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm = 'HS256')
                if login_user(user):
                    load_user(user.id)
                return jsonify(status='success', message = 'User successfully logged in.', id=user.id, token=token)
            return jsonify(errors="Invalid username or password")
        except Exception as e:
            print(e)
            return jsonify(errors='An error occurred while processing your request'), 500
    return jsonify(errors='Invalid request method'), 405



@app.route('/api/v1/auth/logout', methods = ['POST','GET'])
@login_required
def logout():
    try:
        token = request.headers.get('Authorization').split(" ")
        if len(token) == 2:
            if token[0].lower() == "bearer":
                payload = jwt.decode(token[1])
                user_id = ACTIVE.get(payload.get('sub'), None)
                if user_id is not None:
                    ACTIVE.pop(user_id)
        logout_user()
        return jsonify(message = "User sucessfully logged out.")
    except Exception as e:
        print(e)
        return jsonify(errors='An error occurred while processing your request'), 500


# @requires_auth
@app.route('/api/v1/users/<userid>', methods=["GET"])
def user_profile(userid):
    userid = eval(userid)
    token = request.headers.get('Authorization')
    parts = token.split()
    if len(parts) == 2:
        if parts[0].lower() == "bearer":
            try:
                payload = jwt.decode(parts[1], app.config['SECRET_KEY'], algorithms=["HS256"])
                user = ACTIVE.get(userid, None)
                user_id = payload.get('sub')
                if user is not None and userid == user_id:
                    followers = db.session.query(Follows).filter_by(user_id=user_id).count()
                    posts = db.session.query(Posts).filter_by(user_id=user_id).count()
                    data = {
                        "firstname":user.firstname,
                        "lastname":user.lastname,
                        "email":user.email,
                        "location":user.location,
                        "biography":user.biography,
                        "username":user.username,
                        "posts": posts,
                        "followers": followers,
                        "date": user.joined_on.strftime("%d %b %Y"),
                        "image_url": user.profile_photo
                    }
                    photos = db.session.query(Posts.photo).filter_by(user_id=user_id).all()
                    return jsonify(status="success", user=data, photos=photos)
            except jwt.ExpiredSignatureError:
                return jsonify(status="error", type="expired", message="Expired Token")
        else:
            return jsonify(status="error", type="invalid_token", message="Invalid Token type")
    return jsonify(status="error", type="invalid_authorization", message="Unable to fulfill request")


@app.route('/api/v1/users/<user_id>/posts', methods=['POST'])
@login_required
def create_post(user_id):
    form = PostForm()
    
    if request.method=="POST" and form.validate_on_submit:
        try:
            photo = request.files["photo"] or form.photo.data #  When these green parts are commented out the function works in postman. #need to check if this will work when actual file is uploaded
            caption= form.caption.data.strip()
            
            file_in = secure_filename(photo.filename)
            name, ext = file_in.split(".") 
            filename = name + "_" + datetime.strftime(datetime.now(),"%Y-%m-%dT%H-%M-%S") + f".{ext}"

            post= Posts(caption=caption, photo = filename, user_id= user_id) #  When these green parts are commented out the function works in postman. #need to check if this will work when actual file is uploaded
            db.session.add(post)
            db.session.commit()
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #  When these green parts are commented out the function works in postman. #need to check if this will work when actual file is uploaded
            return jsonify(message="Successfully created a new post"), 201
        except Exception as e:
                db.session.rollback()
                print(e)
                return jsonify(errors = f"Error creating post: {e}")
    else:
        return jsonify(errors = "Invalid request method"), 405

# @login_required
@app.route("/api/v1/generate-token")
def generate_token():
    timestamp = datetime.utcnow()
    if current_user is not None:
        payload = {
            "sub": current_user.id,
            "iat": timestamp,
            "exp": timestamp + timedelta(days=7)
        }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify(token=token)


def update_exp(id):
    exp = ACTIVE[id]
    exp = exp + timedelta(days=7)
    

@app.route('/api/v1/users/<user_id>/posts', methods=['GET'])
def getUserPost(user_id):
    if request.method=="GET":
            try:
                temp = Posts.query.filter_by(user_id=user_id).all()
                posts= []
                for post in temp:
                    p={"id":post.id, "user_id": post.user_id, "photo": post.photo,"description": post.caption, "created_on":post.created_on }
                    posts.append(p)
                if posts is None:
                    return jsonify(message="No posts found")
                return jsonify(posts= posts)
            except Exception as e:
                print(e)
                return jsonify(message="Error retrieving posts")
    return jsonify(errors = "Invalid request method"), 405


@app.route('/api/users/<user_id>/follow', methods=['POST'])# Currently not functional. Currently working on it to get it working
@login_required
def follow(user_id):
    if request.method=="POST":
        if g.current_user is not None:
            print(g.current_user)
            if g.current_user.id!= user_id:
                try:
                    follower= g.current_user
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
                    print(e)
                    return jsonify(errors = f"Internal Error: {e}")
            else:
                return jsonify(errors = f"You can't follow yourself.")
    else:
         return jsonify(errors = "Invalid request method"), 405


@app.route('/api/v1/posts', methods=['GET'])
def getPosts():
    if request.method=="GET":
        allPosts = db.session.query(Posts).order_by(desc(Posts.id)).all()
        posts= []
        for post in allPosts:
            id=post.id
            author = dict(zip(('username','profile_photo'),(db.session.query(Users.username, Users.profile_photo).filter_by(id=post.user_id).first())))
            liked = db.session.query(Likes).filter_by(user_id=post.user_id).filter_by(post_id=id).first() is not None
            likes= db.session.query(Likes).filter_by(post_id = id).count()
            p={"liked":liked, "profile_photo":author['profile_photo'], "username": author['username'], "id":id, "user_id": post.user_id, "photo": post.photo,"caption": post.caption, "created_on":post.created_on.strftime("%d %b %Y"),"likes":likes}
            posts.append(p)
        return jsonify(status="success", posts = posts), 200
    return jsonify(errors = "Invalid request method"), 405


@app.route('/api/v1/posts/<post_id>/like', methods=['POST']) # Currently not functional. Currently working on it to get it working
@login_required
# @requires_auth
def like_post(post_id):
    if request.method=="POST":
        like = Likes(post_id=post_id, user_id=current_user.id)
        db.session.add(like)
        db.session.commit()
        return jsonify(status="success", message="Post liked!"), 200
    return jsonify(errors = "Invalid request method"), 405
            

@app.route('/api/v1/posts/<post_id>/unlike', methods=['POST']) # Currently not functional. Currently working on it to get it working
@login_required
# @requires_auth
def unlike_post(post_id):
    if request.method=="POST":
        # find like and delete it
        like = db.session.query(Likes).filter_by(post_id=post_id, user_id=current_user.id)
        db.session.delete(like)
        db.session.commit()
        return jsonify(status="success", message="Post unliked!"), 200
    return jsonify(errors = "Invalid request method"), 405


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



