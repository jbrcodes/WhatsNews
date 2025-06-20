# /jbrbabel/blues/public.py

from flask import Blueprint, current_app


bp = Blueprint('public', __name__)


@bp.route('/')
def home():
    return 'This is Home!' + ' <br><br> ' + current_app.config['DEEPL_API_KEY']