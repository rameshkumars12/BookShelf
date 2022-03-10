import pyrebase
from flask import *
import os
from functools import wraps
from Detect_Text import Book_Image
from Book_Scrapper import book_scrapper

config= {
  "apiKey": "",
  "authDomain": "book-shelf-by-rameshkumar.firebaseapp.com",
  "projectId": "book-shelf-by-rameshkumar",
  "storageBucket": "book-shelf-by-rameshkumar.appspot.com",
  "messagingSenderId": "",
  "appId": "",
  "measurementId": "",
    "databaseURL" : " "
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


app = Flask(__name__)
app.secret_key = os.urandom(24)

#decorator to protect routes
def isAuthenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #check for the variable that pyrebase creates
        if not auth.current_user != None:
            return redirect(url_for('signup'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/my_shelf", methods=["GET","POST"])
def my_shelf():
    book_detail = " "
    if request.method == "POST":
        imagefile = request.files["imagefile"]
        image_predict = Book_Image(imagefile)
        book_details = book_scrapper(image_predict)
        book_detail = book_details
    return render_template("my_shelf.html", tables=[book_detail])



# SignUp Route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        #get the request from data
        email = request.form["email"]
        password = request.form["password"]
        try:
            #create the user
            auth.create_user_with_email_and_password(email, password)
            #login the user right away
            user = auth.sign_in_with_email_and_password(email, password)
            #session
            user_id = user['idToken']
            user_email = email
            session['usr'] = user_id
            session["email"] = user_email
            return redirect("/my_shelf")
        except:
            return render_template("login.html", message="The email is already taken, try another one, please" )

    return render_template("signup.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get the request data
        email = request.form["email"]
        password = request.form["password"]
        try:
            # login the user
            user = auth.sign_in_with_email_and_password(email, password)
            # set the session
            user_id = user['idToken']
            user_email = email
            session['usr'] = user_id
            session["email"] = user_email
            return redirect("/my_shelf")

        except:
            return render_template("login.html", message="Wrong Credentials")

    return render_template("login.html")

#logout route
@app.route("/logout")
def logout():
    #remove the token setting the user to None
    auth.current_user = None
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
