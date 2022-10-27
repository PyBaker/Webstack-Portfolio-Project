#!/usr/bin/env python3
"""Starts the flask app that exposes APIs for this project"""
#from api.v1.views import app_views
from flask import Flask, make_response, jsonify, request, Blueprint
from flask_cors import CORS
import os
from tables import RegisteredVoters, Post, Aspirants, Voters
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

username = 'rod'
password = 'r'
str1 = f'mysql://{username}:{password}@localhost:3306/VOTEAPP'  # Holds database info
engine = create_engine(str1)
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app_views.route('/aspirants/<post_name>', methods=['GET', 'POST', 'PUT'])
def get_aspirants(post_name):
    """Returns a list of candidates vying and their information"""

    if request.method == 'GET':
        #req = request.get_json()
        #if not req:
        #    return make_response(jsonify({'error': 'Data is not a valid json'}))
        # if "post_name" not in req:
        #    return make_response(jsonify({'error': 'Please input the post name'}))

        # post_name = req['post_name']
        query = session.query(Aspirants).filter(Aspirants.post_name == post_name).all()

        return make_response(jsonify([res.to_dict() for res in query]), 200)


@app_views.route('/aspirants/<asp_no>', methods=['GET', 'PUT'])
def get_aspirant(asp_no):
    """Returns information on a particular aspirant"""

    if request.method == 'GET':
        #req = request.get_json()
        #if not req:
        #    return make_response(jsonify({'error': 'Data is not a valid json'}))
        #if 'asp_no' not in req:
        #    return make_response(jsonify({'error': 'Please input the aspirant number'}))

        #asp_no = req['asp_no']
        #print(type(asp_no))
        #print(asp_no)
        aspirant = session.query(Aspirants).filter(Aspirants.asp_no == int(asp_no)).first()

        return make_response(jsonify(aspirant.to_dict()), 200)

@app_views.route('/vote', methods=['PUT'])
def vote():
    """allows registered voters to vote for an aspirant"""

    req = request.get_json()
    if not req:
        return make_response(jsonify({'error': 'Data is not a valid json'}), 400)

    
    # confirm aspirants  and post details
    if "post_name" not in req:
        return make_response(jsonify({'error': 'Please pick a post to vote'}), 400)
    if "asp_no" not in req:
        return make_response(jsonify({'error': 'Please choose a candidate to vote for'}), 400)

    asp_no = req['asp_no']
    post_name = req['post_name']
    aspirant = session.query(Aspirants).filter(Aspirants.asp_no == asp_no).first()
    if not aspirant:
        return make_response(jsonify({'error': 'Please choose a valid candidate'}), 400)

    
    # confirm voter details
    if "id_no" not in req:
        return make_response(jsonify({'error': 'Please log in first to be able to vote'}), 400)
    id_no = req['id_no']
    if "reg_no" not in req:
        return make_response(jsonify({'error': 'Missing registration number'}), 400)
    reg_no = req['reg_no']
    r_voter = session.query(RegisteredVoters).filter(RegisteredVoters.reg_no == reg_no).first()
    if not r_voter:
        return make_response(jsonify({'error': 'Not a registered voter'}))

    # confirm voting duplicates
    voter = session.query(Voters).filter(Voters.reg_no == reg_no).first()
    if not voter:
        voter = Voters(id_no=id_no, reg_no=reg_no)
        setattr(voter, post_name, True)
        session.add(voter)
        session.commit()
    else:
        # check if fully voted
        if voter.Status == "V":
            return make_response(jsonify({'error': 'Already completed voting'}), 400)
        # check if voted for this post
        if getattr(voter, post_name):
            return make_response(jsonify({'error': 'Cannot vote for this candidate twice'}), 400)
        # vote
        setattr(voter, post_name, True)
        # increase aspirant number of votes
        if aspirant.no_of_votes:
            aspirant.no_of_votes += 1
        else:
            aspirant.no_of_votes = 1

        # if fully voted after this, change status to V
        status = 0
        for post in ["president", "senator", "governor", "mp"]:
            if getattr(voter, post):
                status = 1
        if status == 0:   
            voter.Status = "V"
    
    session.commit()

    return make_response(jsonify({'res': 'You have successfully voted!'}), 200)

    


# host and port
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5001)

# Instantiate a flask app variable
app = Flask(__name__)

# register the blueprint to the flask instance
app.register_blueprint(app_views)

# app configurations
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False

# cross-origin resource sharing
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


# create route for error handling
@app.errorhandler(404)
def page_not_found(error):
    """renders a custom error message for non-existent resources"""
    return make_response(jsonify({'error': 'Not found'}), 404)


# run flask app
if __name__ == "__main__":
    """Runs the flask app"""
    app.run(host=host, port=port, debug=True, threaded=True)
