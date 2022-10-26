#!/usr/bin/env python3
"""Creates the Blueprint used for api views"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# import all views here