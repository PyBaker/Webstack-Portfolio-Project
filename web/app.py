"""
Defines routes of the project
"""
import secrets
from processpass import encryptpass 
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy.orm import sessionmaker
from tables import RegisteredVoters, Post, Aspirants, Voters, Admin
from flask import Flask, flash, request, render_template, redirect, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

# connects to database
username = 'rod'
password = 'r' 
str1 = f'mysql://{username}:{password}@localhost:3306/VOTEAPP'  # Holds database info
engine = create_engine(str1)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)
app.secret_key = secrets.token_bytes()

# enable user login
login_manager = LoginManager()
login_manager.init_app(app)


# return current user
@login_manager.user_loader
def load_user(user_id):
    """returns the current logged in user id"""

    return session.query(RegisteredVoters).filter(RegisteredVoters.id == int(user_id)).first()

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
        #print(type(login_password))
        #return f'{login_password}'
        
        # check if admin -- take to admin panel
        admin = session.query(Admin).filter(Admin.id == int(login_userid)).first()        
        if admin:
            if admin.Password.decode('ascii') != login_password:
                return 'Wrong password!'
            login_user(admin)
            return redirect('/admin_panel')
        else:
            # get user
            user = load_user(int(login_userid))
            #  Check if user in Database and confirm login details
            if not user:
                return 'Not a registered voter!'
            if user.Password.decode('ascii') != login_password:
                return 'Wrong password!'

            # Take to voting_screen if casted votes are less that 6
            voter = session.query(Voters).filter(Voters.id == int(login_userid)).first()
            if (not voter) or (voter.status == "NV"):
                login_user(user)
                return redirect('/voting_screen')
            else:
                # take to results page??
                return redirect('/results_page')
    return render_template('login_page.html')


@app.route('/logout')
@login_required
def logout():
    """Logs out the current user"""
    logout_user()
    return 'You are now logged out!'


@app.route('/register-users', methods=['GET', 'POST'])
def register_user():
    """
    Handles registration of users
    """

    # make this page only available to admins -- do the same for the other admin page
    if request.method == "GET":
        admin_id = current_user.id
        admin = session.query(Admin).filter(Admin.id == int(admin_id)).first()
        if not admin:
            flash('Admin Page! Please visit the log in page to log in')
            return redirect('/voting_screen')
            # redirect to voting screen
    if request.method == "POST":
        id_no = request.form.get("id_no")
        firstname = request.form.get("first_name").upper()
        middlename = request.form.get("middle_name").upper()
        lastname = request.form.get("last_name").upper()
        location = request.form.get("location").upper()
        password = request.form.get("password")
        email = request.form.get("email")

        # Writing to the database
        User = RegisteredVoters()
        User.id = int(id_no)
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

    # check if aspirant is a registered voter first
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
        # get aspirant from registered voters -- check if exists
        Aspirant = Aspirants()
        Aspirant.id = idno
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
@login_required
def select_asp():
    """
    Takes you to aspirant voting page
    """
    if request.method == 'POST':
        # print(request.form)
        # print(list(request.form))
        asp = list(request.form)[0]
        # print(asp)
        page_to_load = 'vote_' + asp + '.html'
        # print(page_to_load)
        # name = data_with_president_names_????
        # post_to_display = 'president'

        name = ['Chakulu','Henry','Paul'] # Something like This
        # data = session.query(Aspirants).filter(Aspirants.post_name == 'president')
        data = session.query(Aspirants.asp_no, Aspirants.First_Name, Aspirants.Middle_Name, Aspirants.Last_Name).filter(Aspirants.post_name == asp).all()
        # print(f"this is the data \n\n {data} \n\n")
        return render_template(page_to_load, candidate_list_president=list(data))
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

@app.route('/vote_president')
def vote_president():
    """
    Takes you to Aspirant page
    """
    return render_template('vote_president.html')


@app.route('/vote_senator')
def vote_senator():
    """
    Takes you to Aspirant page
    """
    return render_template('vote_senator.html')


@app.route('/vote_mca')
def vote_mca():
    """
    Takes you to Aspirant page
    """
    return render_template('vote_mca.html')


@app.route('/vote_mp')
def vote_mp():
    """
    Takes you to Aspirant page
    """
    return render_template('vote_mp.html')


@app.route('/vote_woman_rep')
def vote_woman_rep():
    """
    Takes you to Aspirant page
    """
    return render_template('vote_woman_rep.html')


@app.route('/vote_governor')
def vote_():
    """
    Takes you to admin panel
    """
    return render_template('vote_governor.html')




@app.route('/admin_panel')
def admin_panel():
    """
    Takes you to admin panel
    """
    return render_template('admin_panel.html')


@app.route('/voting_screen')
@login_required
def voting_screen():
    """
    Takes you to voting screen
    """
    return render_template('voting_screen.html',
        user_f_name=current_user.First_Name,
        user_l_name=current_user.Last_Name,
        id=current_user.id,
        reg_no=current_user.reg_no
        )


@app.route('/results_page')
def results_page():
    """
    Handles Results page
    """
    return render_template('results_page.html')

if __name__ == "__main__":
    app.run(port=5000)
