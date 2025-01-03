# type: ignore

from flask import Blueprint

auth = Blueprint("auth", __name__, template_folder="templates")

from . import forms, views, errors
