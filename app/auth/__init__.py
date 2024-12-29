# type: ignore

from flask import Blueprint

auth = Blueprint("auth", __name__)

from . import forms, views, errors
