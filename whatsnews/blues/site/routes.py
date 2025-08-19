# /whatsnews/blues/site/routes.py

from flask import abort, Blueprint, g, redirect, request, url_for
import peewee
from whatsnews.models import db
from whatsnews.models.Site import Site
from whatsnews.blues.site.forms import SiteForm


PAGE_SIZE = 10


bp = Blueprint('site', __name__, url_prefix='/sites')


@bp.route('/')
def index():
    page_no = int( request.args.get('page_no', 1) )
    sites = Site.select().order_by(Site.name_sort).paginate(page_no, PAGE_SIZE)

    return g.jinjax_catalog.render('admin.pages.Site.Index', sites=sites)


@bp.route('/<int:id>/view')
def view(id):
    site = Site.get_or_none(id)
    if site is None:
        abort(404)

    return g.jinjax_catalog.render('admin.pages.Site.View', site=site)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = SiteForm()
    if form.validate_on_submit():
        site = Site()
        form.populate_obj(site)
        # http://docs.peewee-orm.com/en/latest/peewee/database.html#managing-transactions
        with db.atomic() as txn:
            try:
                site.save()
            except peewee.IntegrityError as e:
                txn.rollback()
                form.name.errors = [ str(e) ]  # FIX ME: 'name' (and others?) should be unique 
                return g.jinjax_catalog.render('admin.pages.Site.Form', form=form)
        return redirect( url_for('admin.site.index') )
    else:
        return g.jinjax_catalog.render('admin.pages.Site.Form', form=form)


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    site = Site.get_or_none(id)
    if site is None:
        abort(404)

    form = SiteForm(obj=site)
    if form.validate_on_submit():
        form.populate_obj(site)
        # http://docs.peewee-orm.com/en/latest/peewee/database.html#managing-transactions
        with db.atomic() as txn:
            try:
                site.save()
            except peewee.IntegrityError as e:
                txn.rollback()
                form.name.errors = [ str(e) ]  # FIX ME: 'name' (and others?) should be unique 
                return g.jinjax_catalog.render('admin.pages.Site.Form', form=form, site_id=id)
        return redirect( url_for('admin.site.index') )
    else:
        return g.jinjax_catalog.render('admin.pages.Site.Form', form=form, site_id=id)


@bp.route('/<int:id>/delete')
def delete(id):
    site = Site.get_or_none(id)
    if site is None:
        abort(404)
    
    site.delete_instance()

    return redirect( url_for('admin.site.index') )