from flask import flash, jsonify, redirect, render_template, request, session, url_for, g, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from flaskr import db
from flaskr.user_models import User
from flaskr.users import bp
from .forms import LoginForm, RegisterForm, PasswordChangeForm, RequestPasswordResetForm, ResetPasswordForm
from flaskr.email import send_email

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

@bp.route('/register', methods=['GET', 'POST'])# dodać ograniczenia dostępu
@login_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password = form.password.data 
                )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm your email address.',
                'users/email/confirm', user=user, token=token)
        flash('The email message has been sent on {}'.format(user.email))
        return redirect(url_for('staff.search_title'))
    return render_template('users/register.html', form=form)

@bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('staff.search_title'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Your email address has been confirmed. Thanks.')
    else:
        flash('Confirmation link is outdated or non valid.')
    return redirect(url_for('users.login'))


@bp.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'users'\
            and request.endpoint != 'static':
        return redirect(url_for('users.unconfirmated'))

@bp.route('/unconfirmated')
def unconfirmated():
    if current_user.is_anonymous:
        pass
    elif current_user.confirmed:
        return redirect(url_for('staff.search_title'))
    return render_template('users/unconfirmed.html')

@bp.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm your email address.',
            'users/email/confirm', user=current_user, token=token)
    flash('New confirmation email has been sent.')
    return redirect('url_for(staff.search_title)')

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('staff.search_title'))
        else:
            flash('Invalid password')
    return render_template('users/change_password.html', form=form)

@bp.route('/reset', methods=['GET', 'POST'])
def request_password_reset():
    if not current_user.is_anonymous:
        return redirect(url_for('staff.search_title'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                    'users/email/reset_password', 
                    user=user, token=token)
        flash('Please check your email')
        return redirect(url_for('users.login'))
    return render_template('users/reset_password.html', form=form)

@bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('staff.search_title'))
    form = ResetPasswordForm() 
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been changed')
            return redirect(url_for('users.login'))
        else:
            return redirect(url_for('staff.search_title'))
    return render_template('users/password_reset_new.html', form=form)
