import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, cursor = get_db()

        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            cursor.execute("SELECT id FROM users WHERE username = '{}';".format(username))
            if cursor.fetchone() is not None:
                error = 'User {} is already registered.'.format(username)

        if error is None:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES ('{}', '{}');".format(username, generate_password_hash(password))
                    )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, cursor = get_db()
        error = None
        cursor.execute(
            "SELECT * FROM users WHERE username = '{}'".format(username)
        )

        # same issue as described in blog.py in line 20
        cols = ['id', 'username', 'password']
        vals = cursor.fetchone()
        if vals: user = {cols[i]: vals[i]  for i in xrange(len(cols)) }
        else: user = None

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, cursor = get_db()
        cursor.execute(
            "SELECT * FROM users WHERE id = '{}'".format(user_id)
        )
        cols = ['id', 'username', 'password']
        vals = cursor.fetchone()
        if vals: g.user = {cols[i]: vals[i]  for i in xrange(len(cols)) }
        else: g.user = None


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
