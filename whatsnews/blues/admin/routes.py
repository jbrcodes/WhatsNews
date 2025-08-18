# /whatsnews/blues/admin/routes.py

from flask import Blueprint, g



bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
def dashboard():
    return g.jinjax_catalog.render('admin.pages.Dashboard')