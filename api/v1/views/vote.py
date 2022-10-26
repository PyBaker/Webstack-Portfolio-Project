#!/usr/bin/env python3
"""Defines APIs that implement the voting feature"""
from api.v1.views import app_views
from flask import jsonify, make_response, request
from Models.tables import RegisteredVoters, Post, Aspirants, Voters
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

username = 'rod'
password = 'r'
str1 = f'mysql://{username}:{password}@localhost:3306/VOTEAPP'  # Holds database info
engine = create_engine(str1)
DBSession = sessionmaker(bind=engine)
session = DBSession()


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
        voter[f'{post_name}'] = True
        session.add(voter)
        session.commit()
    else:
        # check if fully voted
        if voter.status == "V":
            return make_response(jsonify({'error': 'Already completed voting'}), 400)
        # check if voted for this post
        if voter[f'{post_name}']:
            return make_response(jsonify({'error': 'Cannot vote for this candidate twice'}), 400)
        # vote
        voter[f'{post_name}'] = True
        # if fully voted after this, change status to V
        status = 0
        for post in ["president", "senator", "governor", "mp"]:
            if voter[post] == False:
                status = 1
        if status == 0:   
            voter.status = "V"
    
    session.commit()

    return make_response(jsonify({'res': 'You have successfully voted!'}), 200)
    
