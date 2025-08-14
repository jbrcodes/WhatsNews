# /whatsnews/blues/public.py

from flask import Blueprint, render_template


bp = Blueprint('public', __name__)


@bp.route('/')
def home():
    from whatsnews.models.Site import Site

    # Warning! This does N+1 queries!!
    sites = Site.select().order_by(Site.name_sort)

    return render_template('home.html', sites=sites)


@bp.route('/about')
def about():
    return render_template('about.html')