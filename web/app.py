"""
Defines routes of the project
"""
from processpass import encryptpass 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import RegisteredVoters, Post, Aspirants
from flask import Flask, request, render_template, redirect

# connects to database
username = 'rod'
password = 'r'
str1 = f'mysql://{username}:{password}@localhost:3306/VOTEAPP'  # Holds database info
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
    # Redirecting home to login_page
    return redirect('/login')


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
        idno = request.form.get("id_no")
        firstname = request.form.get("first_name").upper()
        middlename = request.form.get("middle_name").upper()
        lastname = request.form.get("last_name").upper()
        location = request.form.get("location").upper()
        password = request.form.get("password")
        email = request.form.get("email")

        # Writing to the database
        User = RegisteredVoters()
        User.id_no = idno
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

    return render_template('registration_page.html')


@app.route('/register-aspirants', methods=['GET', 'POST'])
def register_aspirants():
    """
    Handles registration of Aspirants
    """
    if request.method == "POST":
        idno = request.form.get("idno")
        postname = request.form.get("post_name").upper()
        firstname = request.form.get("first_name").upper()
        middlename = request.form.get("middle_name").upper()
        lastname = request.form.get("last_name").upper()
        location = request.form.get("location").upper()
        password = request.form.get("password")
        email = request.form.get("email")

        # Writing to the database
        Aspirant = Aspirants()
        Aspirant.id_no = idno
        Aspirant.Post_Name = postname
        Aspirant.First_Name = firstname
        Aspirant.Middle_Name = middlename
        Aspirant.Last_Name = lastname
        Aspirant.Location = location
        Aspirant.Password = encryptpass(password)
        Aspirant.Email = email
        
        # Commiting to the database
        session.add(Aspirant)
        session.commit()

        return "You have successfully registered aspirant"
    return render_template('aspirant.html')


@app.route('/register-post', methods=['GET', 'POST'])
def register_post():
    """
    Handles registration of Posts
    """
    if request.method == 'POST':
        postname = request.form.get("post_name").upper()

        #Writing to the database
        post = Post(Post_Name=postname)

        #Comitting to database
        session.add(post)
        session.commit()
        return "You have successfully registered the post"

    return render_template('post.html')


if __name__ == "__main__":
    app.run(port=5000)
