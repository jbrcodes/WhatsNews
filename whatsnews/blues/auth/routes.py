# /whatsnews/blues/auth/routes.py

from flask import Blueprint, current_app, flash, g, redirect, request, session, url_for
from whatsnews.blues.auth.forms import LoginForm
from whatsnews.models.User import User
from whatsnews.blues.auth.models import user_auth


bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return g.jinjax_catalog.render('public.pages.Login', form=form)
    else:
        if form.validate_on_submit():
            user = User.login(form.username.data, form.password.data)
            if user:
                user_auth.login(user)

                # https://flask-session.readthedocs.io/en/latest/security.html#session-fixation
                current_app.session_interface.regenerate(session)

                next_url = request.form.get('next', '')
                url = next_url if next_url != '' else url_for('public.home')
                flash('Login succeeded', 'success')
                return redirect(url)
            else:
                flash('Login failed', 'error')
                form.username.data = form.password.data = ''  # hack that only kinda works
                return g.jinjax_catalog.render('public.pages.Login', form=form), 401
        else:
            flash('Login failed', 'error')
            return g.jinjax_catalog.render('public.pages.Login', form=form), 401


@bp.route('/logout')
def logout():
    user_auth.logout()
    return redirect( url_for('public.home') )
