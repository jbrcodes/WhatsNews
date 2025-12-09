# /bn/blues/public.py

from flask import Blueprint, g
from bn.models.Post import Post
from bn.models.Site import Site

bp = Blueprint('public', __name__)


@bp.route('/')
def home():

    # Warning! This does N+1 queries!!
    sites = Site.select().where(Site.is_active).order_by(Site.name_sort)
    for site in sites:
        site.posts = Post.select().where(Post.site_id == site.id).order_by(Post.id)  # (hack!)

    return g.jinjax_catalog.render('public.pages.Home', sites=sites)


@bp.route('/about')
def about():
    return g.jinjax_catalog.render('public.pages.About')