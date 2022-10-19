"""
Defines routes of the project
"""
from processpass import encryptpass 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import RegisteredVoters
from flask import Flask, request, render_template

# connects to database
str1 = 'mysql://root:''@localhost:3306/VOTEAPP'  # Holds database info
engine = create_engine(str1)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

# allow both GET and POST requests
@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    if request.method == 'POST':
        language = request.form.get('language')
        framework = request.form.get('framework')
        return f'''
        <h1> The Language value is: {language} </h1>
        <h1> The language value is: {framework} </h1>'''
    return '''
              <form method="POST">
                  <div><label>Language: <input type="text" name="language"></label></div>
                  <div><label>Framework: <input type="text" name="framework"></label></div>
                  <input type="submit" value="Submit">
              </form>'''
@app.route('/')
@app.route('/home')
def home():
    """
    Holds the landing Page
    """
    return "This is the landng page"


@app.route('/login')
def login():
    """
    Handles user authentification into the system
    """
    return render_template('login_page.html')


@app.route('/register-users', methods=['GET', 'POST'])
def register_user():
    """
    Handles registration of users
    """
    if request.method == "POST":
        firstname = request.form.get("first_name")
        middlename = request.form.get("middle_name")
        lastname = request.form.get("last_name")
        location = request.form.get("location")
        password = request.form.get("password")
        email = request.form.get("email")

        # Writing to the database
        User = RegisteredVoters()
        User.First_Name = firstname
        User.Middle_Name = middlename
        User.Last_Name = lastname
        User.Location = location
        User.Password = encryptpass(password)
        User.Email = email
        
        # Comitting User to database
        session.add(User)
        session.commit()
        return "You have Successfully Registred"

    return render_template('form.html')


@app.route('/register-aspirants')
def register_aspirants():
    """
    Handles registration of Aspirants
    """
    return "I want to register aspirants"


@app.route('/register-post')
def register_post():
    """
    Handles registration of Posts
    """
    return "I want to register posts"


if __name__ == "__main__":
    app.run(port=5000)
