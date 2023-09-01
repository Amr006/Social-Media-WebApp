from sqlite3 import IntegrityError
from flask import Flask, request, url_for, redirect, render_template, session, flash
from datetime import timedelta , datetime
import base64
import utils, os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import db , validators
import datetime

app = Flask(__name__)
app.secret_key = "findwhatyouloveandletitKILLYOU"
app.permanent_session_lifetime = timedelta(days=5)
connection = db.connect_to_database()
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["50 per minute"])

@app.route("/")
def display_posts():
    check_login = session.get('logged_in', False)
    check_register = session.get('registered', False)
    if check_login and check_register:
        # try:
        posts = db.get_all_posts(connection)
        return render_template("posts.html",posts = posts)
        # except IntegrityError :
        #     flash("there are no posts yet please go try and add a post!","success")
        #     return redirect(url_for('add-post'))
    elif check_register and not check_login :
        flash("Please Log in First" ,"info")
        return redirect(url_for('login'))
    else:
        flash("Please Register First" ,"info")
        return redirect(url_for('register'))

@app.route("/display_post/<post_id>", methods = ["GET"])
def display_post(post_id):
    check_login = session.get('logged_in', False)
    check_register = session.get('registered', False)
    if check_register and not check_login :
        return redirect(url_for('login'))
    elif not check_register and not check_login:
        return redirect(url_for('register'))
    try:
        post = db.get_post_by_post_id(connection, post_id)
        return render_template('display_post.html', post=post)
    except IntegrityError :
        flash("Sorry there are no posts yet")
        return redirect(url_for("display_posts"))

app.route('/search/<userName>')
def searchForUser(userName):
    try:
        user = db.get_user_by_username(connection,userName)
    except IntegrityError:
        flash('Not Found')
        return render_template("searchPage.html" , user = "Not Found")
    return render_template("searchPage.html" , user = user) 

@app.route("/add_post", methods = ["POST", "GET"])
def add_post():
    check_login = session.get('logged_in', False)
    check_register = session.get('registered', False)
    if check_register and not check_login :
        return redirect(url_for('login'))
    elif not check_register and not check_login:
        return redirect(url_for('register'))
        
    if request.method == "POST":
        image_for_post = request.files['image']                   

        if not image_for_post or image_for_post.filename == '':
            flash('Nothing was Selected, please Choose something',"danger")
            return render_template('add_post.html')
    
        if not validators.allowed_file(image_for_post.filename) or not validators.allowed_file_size(image_for_post):
            flash("Invalid File is Uploaded", "danger")
            return render_template("add_post.html")
        
        description_for_post = request.form['description']
        image_data = base64.b64encode(image_for_post.read()).decode('utf-8')
        image_ext = image_for_post.filename.split(".")[1]
        user_id = session['user_id']
        db.add_post(connection, user_id, description_for_post,image_data,image_ext , datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        flash('Post Created Successfully!!',"success")
        return redirect(url_for('display_posts'))

    return render_template("add_post.html")

@app.route("/add-comment/<post_id>", methods = ["POST", "GET"])
def add_comment(post_id):

    check_login = session.get('logged_in', False)
    check_register = session.get('registered', False)

    if check_register and not check_login :
        return redirect(url_for('login'))
    elif not check_register and not check_login:
        return redirect(url_for('register'))
    
    if request.method == "POST":

        user_id = session['user_id'] 
        comment_content = request.form['comment']

        db.add_comment_to_db(connection, user_id, comment_content)
        return redirect(url_for("display_post"), post_id = post_id)
    
    return redirect(url_for('display_post', post_id = post_id))



# Authentication

@app.route("/register", methods=["GET", "POST"])
@limiter.limit("10 per minute") 
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if not utils.is_strong_password(password):
            flash("Sorry You Entered a weak Password Please Choose a stronger one", "danger")
            return render_template('register.html')
        
        token = db.get_user_by_username(connection, username)

        if not token : 
            hashedPassword = utils.hash_password(password)
            db.add_user(connection, username, hashedPassword) # if username in database already in database it will return an error to terminate the server
            session['username'] = username
            session['logged_in'] = False
            session['registered'] = True
            session['user_id'] = db.get_user_by_username(connection, username)[0]
            flash("Account Created Successfully!!", "success")
            return redirect(url_for("login"))
        else: 
            flash('User already exists!',"danger")
            session['registered'] = True
            return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute") 
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.get_user_by_username(connection, username)
        if user:
            real_password = user[2]
            if utils.is_password_match(password , real_password):
                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = user[0]
                flash('Welcome '+username,"success")
                return redirect(url_for("display_posts"))
            else:
                flash('Incorrect Password. Please try again.',"danger")
        else:
            flash('User does not exist. Please register!',"danger")
            return redirect(url_for('register'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    flash('Logged Out Successfully!',"success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.init_users(connection)
    db.init_posts(connection)
    db.init_comments(connection)
    app.run(debug=True)
