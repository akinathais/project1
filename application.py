import os
import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json",
                   params={"key": "hJX1a7y70CCsIYEYhgwVrg", "isbns": "9781632168146"})
print(res.json())

from flask import Flask, session, render_template, request, abort, jsonify, redirect, url_for
from flask_session.__init__ import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from markupsafe import escape


def create_app(test_config=None):
    app = Flask(__name__)

# set secret key
app.secret_key = os.urandom(50)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
Database_URL = "postgres://rcttigxsyfnzwd:03ef0b534c015de842f3643c4ac5d400b94a81f173fdbb1f862b351adc99315e@ec2-54-228-250-82.eu-west-1.compute.amazonaws.com:5432/dag6tsfma7d0li"
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# create the user class
class User:
    #id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(56), unique=True) 
    #email = db.Column(db.String(80), unique=True)

    def __init__ (self, id, username, email, password):
        self.id= id
        self.username= username
        self.email= email
        self.password= password

    def __repr__(self):
        return '<User %r>' % self.username

# Create a global variable users
users = []
users.append(User(id=1, username='ana', email='a@a.com', password='batata' ))
users.append(User(id=2, username='hugostoso', email='h@a.com', password='chocolate'))

@app.route("/", methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return 'Logged in X' % escape(session['username'])
    #return 'You are logged in'

    return render_template("index.html") 

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #to remove (pop) previous login when new session start
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']

        # to check if the user is inside the global variable list 
        user = [x for x in users if x.username == username][0]
        #to check if the password given is the same associated with user data 
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        
        #if the user is not found, the page does not start a session
        return render_template('login.html')

    return render_template ("index.html")
     

@app.route("/profile")
def profile():
    session.pop('username', None)
    return render_template ("profile.html")



if __name__ == '__main__':
    app.run()

