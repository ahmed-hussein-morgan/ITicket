from flask import Blueprint

non_tech = Blueprint("non_tech", __name__)

from . import forms, views, errors