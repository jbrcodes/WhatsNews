# /whatsnews/blues/public.py

from flask import Blueprint, g


bp = Blueprint('public', __name__)


@bp.route('/')
def home():
    from whatsnews.models.Site import Site

    # Warning! This does N+1 queries!!
    sites = Site.select().order_by(Site.name_sort)

    return g.jinjax_catalog.render('public.pages.Home', sites=sites)


@bp.route('/about')
def about():
    return g.jinjax_catalog.render('public.pages.About')