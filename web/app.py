"""
Defines routes of the project
"""
from processpass import encryptpass 
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, PendingRollbackError
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


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    Handles user authentification into the system
    """
    if request.method == 'POST':
        login_password = request.form.get('password')
        login_userid = request.form.get('user_id')

        # Check if admin
        #
        # Take to admin panel
        #
        #  Check if user in Database
        #
        # Take to voting_screen if casted votes are less that 6
 
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
        try:
            session.add(User)
            session.commit()
        except PendingRollbackError:
            session.rollback()
            session.add(User)
            session.commit()
        except IntegrityError:
            return f"The user {User.First_Name} has already been registered"

        return f"You have Successfully Registred {User.First_Name}"

    return render_template('registration_page.html')


@app.route('/register-aspirants', methods=['GET', 'POST'])
def register_aspirants():
    """
    Handles registration of Aspirants
    """
    if request.method == "POST":
        idno = request.form.get("id_no")
        postname = request.form.get("post_name")
        firstname = request.form.get("first_name").upper()
        middlename = request.form.get("middle_name").upper()
        lastname = request.form.get("last_name").upper()
        location = request.form.get("location").upper()
        email = request.form.get("email")

        #Query database for post names
        if session.query(Post).filter(Post.Post_Name == postname).first() is None:
            return "Post is yet to be registered"

        # Writing to the database
        Aspirant = Aspirants()
        Aspirant.id_no = idno
        Aspirant.post_name = postname
        Aspirant.First_Name = firstname
        Aspirant.Middle_Name = middlename
        Aspirant.Last_Name = lastname
        Aspirant.Location = location
        Aspirant.Email = email
        
        # Commiting to the database
        try:
            session.add(Aspirant)
            session.commit()
        except PendingRollbackError:
            session.rollback()
            session.add(Aspirant)
            session.commit()
        except IntegrityError:
            return "Aspirant Must Be A Registered Voter"


        return "You have successfully registered aspirant"

    return render_template('registration_page_aspirant.html')


@app.route('/register-post', methods=['GET', 'POST'])
def register_post():
    """
    Handles registration of Posts
    """
    if request.method == 'POST':
        postname = request.form.get("post_name").upper()

        # Writing to the database
        post = Post(Post_Name=postname)

        # Comitting to database
        try:
            session.add(post)
            session.commit()
        except PendingRollbackError:
            session.rollback()
            session.add(post)
            session.commit()
        except IntegrityError:
            return "The post already exists"

        return "You have successfully registered the post"

    return render_template('post.html')


@app.route('/select_asp', methods=['POST', 'GET'])
def select_asp():
    """
    Takes you to aspirant voting page
    """
    if request.method == 'POST':
        asp = list(request.form)[0]
        page_to_load = 'vote_' + asp + '.html'
        # print(page_to_load)
        name = ['Chakulu','Henry','Paul']
        return render_template(page_to_load, candidate_list=name)
    return render_template('voting_screen.html')


@app.route('/vote', methods=['POST', 'GET'])
def sent_vote():
    """
    handles the voting choices
    """
    print(request.form)
    if request.method == 'POST':
        if request.form:
            choice = request.form['uo']
            print(f"voter submitted Candidate no {choice}")
            return render_template('voting_screen.html')
    return redirect(request.referrer)


@app.route('/admin_panel')
def admin_panel():
    """
    Takes you to admin panel
    """
    return render_template('admin_panel.html')


@app.route('/voting_screen')
def voting_screen():
    """
    Takes you to voting screen
    """
    return render_template('voting_screen.html')


@app.route('/results_page')
def results_page():
    """
    Handles Results page
    """
    return render_template('results_page.html')

if __name__ == "__main__":
    app.run(port=5000)
