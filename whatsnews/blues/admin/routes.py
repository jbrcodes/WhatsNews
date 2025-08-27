# /whatsnews/blues/admin/routes.py

from flask import Blueprint, g, redirect, request, url_for
from whatsnews.blues.auth.models import user_auth


bp = Blueprint('admin', __name__, url_prefix='/jbr-admin')


@bp.before_request
def check_for_admin():
    ''' Guard to protect all admin pages '''
    if not user_auth.is_logged_in():
        return redirect( url_for('auth.login', next=request.full_path) )
        

@bp.route('/')
def dashboard():
    return g.jinjax_catalog.render('admin.pages.Dashboard')