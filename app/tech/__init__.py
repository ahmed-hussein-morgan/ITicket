from flask import Blueprint

tech = Blueprint("tech", __name__)

from . import forms, views, errors