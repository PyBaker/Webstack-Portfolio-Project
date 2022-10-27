#!/usr/bin/env python3
"""Defines APIs for interacting with Aspirants' info"""
from api.v1.views import app_views
from flask import jsonify, make_response, request
from Models.tables import RegisteredVoters, Post, Aspirants
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


username = 'rod'
password = 'rodahiA1@'
str1 = f'mysql://{username}:{password}@localhost:3306/VOTEAPP'  # Holds database info
engine = create_engine(str1)
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app_views.route('/aspirants/<post_name>', methods=['GET', 'POST', 'PUT'])
def get_aspirants(post_name):
    """Returns a list of candidates vying and their information"""

    if request.method == 'GET':
        req = request.get_json()
        if not req:
            return make_response(jsonify({'error': 'Data is not a valid json'}))
        if "post_name" not in req:
            return make_response(jsonify({'error': 'Please input the post name'}))

        post_name = req['post_name']
        query = session.query(Aspirants).filter(Aspirants.post_name == post_name).all()

        return make_response(jsonify([res.to_dict() for res in query]), 200)


@app_views.route('/aspirants/<asp_no>', methods=['GET', 'PUT'])
def get_aspirant(asp_no):
    """Returns information on a particular aspirant"""

    if request.method == 'GET':
        req = request.get_json()
        if not req:
            return make_response(jsonify({'error': 'Data is not a valid json'}))
        if 'asp_no' not in req:
            return make_response(jsonify({'error': 'Please input the aspirant number'}))

        asp_no = req['asp_no']
        aspirant = session.query(Aspirants).filter(Aspirants.asp_no == asp_no).first()

        return make_response(jsonify(aspirant.to_dict()), 200)
