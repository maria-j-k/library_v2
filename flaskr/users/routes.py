from flask import flash, jsonify, redirect, render_template, request, session, url_for, g, current_app
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from flaskr import db
from flaskr.user_models import User
from flaskr.users import bp
from .forms import LoginForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('staff.search_title'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('users.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('staff.search_title')
        return redirect(next_page)
    return render_template('users/login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))
