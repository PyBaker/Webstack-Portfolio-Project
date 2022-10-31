"""
Defines routes of the project
"""
import secrets
# from tkinter import TRUE ? QUESTION
from processpass import encryptpass
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy.orm import sessionmaker
from tables import RegisteredVoters, Post, Aspirants, Voters, Admin, myEnum
from flask import Flask, flash, request, render_template, redirect, make_response, jsonify, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import flask_login 

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

@app.route('/test')
def test():
    flash('How far now')
    return('/login')


# return current user
@login_manager.user_loader
def load_user(user_id):
    """returns the current logged in user id"""

    return session.query(RegisteredVoters).filter(RegisteredVoters.id == int(user_id)).first()


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
        #login_user(admin)      
        if admin:
            login_user(admin)
            if admin.Password.decode('ascii') != login_password:
                return 'Wrong password!'
            #login_user(admin)
            return redirect('/admin_panel')
        else:
            # get user
            user = load_user(int(login_userid))
            #  Check if user in Database and confirm login details
            if not user:
                return 'Not a registered voter!'
            if user.Password.decode('ascii') != login_password:
                return 'Wrong password!'

            login_user(user)

            # comment out
            # login_user(user)
            # return redirect('/voting_screen')
            # Take to voting_screen if casted votes are less that 6
            voter = session.query(Voters).filter(Voters.id == int(login_userid)).first()
            #print(voter.Status)
            if voter:
                if voter.Status == myEnum.V:
                    #login_user(user)
                    #return redirect('/voting_screen')
                    # take to results page??
                    return redirect('/results_page')
            return redirect('/voting_screen')
    return render_template('login_page.html')


@app.route('/logout')
@login_required
def logout():
    """Logs out the current user"""
    logout_user()
    return 'You are now logged out!'


@app.route('/register-users', methods=['GET', 'POST'])
#@login_required
def register_user():
    """
    Handles registration of users
    """

    # make this page only available to admins -- do the same for the other admin page
    """if request.method == "GET":
        admin_id = current_user.id
        admin = session.query(Admin).filter(Admin.id == int(admin_id)).first()
        if not admin:
            flash('Admin Page! Please visit the log in page to log in')
            return redirect('/voting_screen')
            # redirect to voting screen"""
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
            session.rollback()
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
            session.rollback()
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
            session.rollback()
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

        id = current_user.id
        voter = session.query(Voters).filter(Voters.id == id).first()
        
        if voter:
            # check if voter is fully voted
            if voter.Status == myEnum.V:
                flash('Already completed voting')
                return redirect('/results_page')

            # check if voter voted for this candidate
            if getattr(voter, asp) is True:
                flash('Cannot vote for this candidate twice')
                return redirect('/voting_screen')

        #name = ['Chakulu','Henry','Paul'] # Something like This
        # data = session.query(Aspirants).filter(Aspirants.post_name == 'president')
        data = session.query(Aspirants.asp_no, Aspirants.First_Name, Aspirants.Middle_Name, Aspirants.Last_Name).filter(Aspirants.post_name == asp).all()
        # print(f"this is the data \n\n {data} \n\n")
        return render_template(page_to_load, candidate_list=list(data))
    return render_template('voting_screen.html')


@app.route('/vote/<post_name>', methods=['POST', 'GET'])
@login_required
def sent_vote(post_name):
    """
    handles the voting choices
    """
    #print(request.form['uo'])
    #print(post_name)
    if request.method == 'POST':    
    # confirm aspirants  and post details
        asp_no = int(request.form['uo'])

        aspirant = session.query(Aspirants).filter(Aspirants.asp_no == asp_no).first()
        
        #print(current_user.keys())
        g_user = current_user.get_id()
        # print(f"user id is: {g_user}")
        """if current_user.is_authenticated:
            print("authenticated")
            g_user = current_user.get_id()
            print(g_user)"""
        # confirm voter details
        id_no = current_user.id
        reg_no = current_user.reg_no

        r_voter = session.query(RegisteredVoters).filter(RegisteredVoters.reg_no == reg_no).first()
        if not r_voter:
            return 'Not a registered voter'

        # confirm voting duplicates
        voter = session.query(Voters).filter(Voters.reg_no == reg_no).first()
        if not voter:
            voter = Voters(id=id_no, reg_no=reg_no)
            setattr(voter, post_name, True)
            session.add(voter)
            session.commit()
        else:
            pass
            # check if fully voted -- moved this to select_asp route/ already in login route
            """print(voter.Status)
            if voter.Status == myEnum.V:
                flash('Already completed voting')
                return redirect('/results_page')"""

            # check if voted for this post -- this logic has been implemented in select_asp route
            """print(getattr(voter, post_name))
            if getattr(voter, post_name) is True:
                flash('Cannot vote for this candidate twice')
                return redirect('/voting_screen')"""
        # vote
        setattr(voter, post_name, True)
        session.commit()
            # increase aspirant number of votes
        if aspirant.no_of_votes == None:
            aspirant.no_of_votes = 1
        else:
            aspirant.no_of_votes += 1

        # if fully voted after this, change status to V
        status = 0
        for post in ["president", "senator", "governor", "mp"]:
            #print(getattr(voter, post))
            if getattr(voter, post) == 0:
                status = 1
                break
        if status == 0:
            voter.Status = myEnum.V
            session.commit()
            return redirect('/results_page')
        
        session.commit()
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
#@login_required
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
    """return render_template('voting_screen.html',
        user_f_name=current_user.First_Name,
        user_l_name=current_user.Last_Name,
        id=current_user.id,
        reg_no=current_user.reg_no
        )"""
    return render_template('voting_screen.html')


@app.route('/results_page')
def results_page():
    """
    Handles Results page
    """

    # get results for all posts and candidates in each post
    def votes(my_list):
        """display votes"""
        if my_list[4] is None:
            my_list[4] = 0

    my_dict = {}

    # president
    p_query = session.query(Aspirants.id, Aspirants.First_Name, Aspirants.Middle_Name, Aspirants.Last_Name, Aspirants.no_of_votes).filter(Aspirants.post_name == "President").order_by(Aspirants.no_of_votes).all()
    presidents = list(map(lambda x: list(x), list(p_query)))
    for p in presidents:
        votes(p)
    my_dict['president'] = presidents

    # governor
    g_query = session.query(Aspirants.id, Aspirants.First_Name, Aspirants.Middle_Name, Aspirants.Last_Name, Aspirants.no_of_votes).filter(Aspirants.post_name == "Governor").order_by(Aspirants.no_of_votes).all()
    governors = list(map(lambda x: list(x), list(g_query)))
    for g in governors:
        votes(g)
    my_dict['governor'] = governors

    # senator
    s_query = session.query(Aspirants.id, Aspirants.First_Name, Aspirants.Middle_Name, Aspirants.Last_Name, Aspirants.no_of_votes).filter(Aspirants.post_name == "Senator").order_by(Aspirants.no_of_votes).all()
    senators = list(map(lambda x: list(x), list(s_query)))
    for s in senators:
        votes(s)
    my_dict['senator'] = senators

    # mp
    m_query = session.query(Aspirants.id, Aspirants.First_Name, Aspirants.Middle_Name, Aspirants.Last_Name, Aspirants.no_of_votes).filter(Aspirants.post_name == "MP").order_by(Aspirants.no_of_votes).all()
    mps = list(map(lambda x: list(x), list(m_query)))
    for m in mps:
        votes(m)
    my_dict['mp'] = mps


    # get voter turnout - number of people who voted
    voters = session.query(Voters).count()

    # get number of total registered voters
    registered_v = session.query(RegisteredVoters).count()

    return render_template('results_page.html', registered_v=registered_v, voters=voters, candidate_update=my_dict)

if __name__ == "__main__":
    app.run(port=5000)
