from sqlite3 import IntegrityError
from flask import Flask, request, url_for, redirect, render_template, session, flash
from datetime import timedelta , datetime
import utils
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import db , validators
app = Flask(__name__)
app.secret_key = "findwhatyouloveandletitKILLYOU"
app.permanent_session_lifetime = timedelta(days=5)
connection = db.connect_to_database()
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["50 per minute"])

@app.route("/")
def index():
   return "This is Web Application of Team18/Amr006 xD"

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
            session['logged_in'] = True
            session['registered'] = True
            session['user_id'] = db.get_user_by_username(connection, username)[0]
            return redirect(url_for('home'))
        else: 
            flash('User already exists!')
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
                return redirect(url_for('home'))
            else:
                flash('Incorrect Password. Please try again.')
        else:
            flash('User does not exist. Please register!')
            return redirect(url_for('register'))
    return render_template("login.html")


app.route('/search/<userName>')
def searchForUser(userName):
    
    try:
        user = db.get_user_by_username(connection,userName)
        
    except IntegrityError:
        flash('Not Found')
        return render_template("searchPage.html" , user = "Not Found")
    
    return render_template("searchPage.html" , user = user)
    

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    flash('Logged Out Successfully!')
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.init_db(connection)
    app.run(debug=True)
