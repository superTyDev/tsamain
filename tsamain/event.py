import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from tsamain.db import get_db

bp = Blueprint('event', __name__, url_prefix='/event')


@bp.before_app_request
def load_logged_in_user():
    userid = session.get('userid')

    if userid is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE userid = ?', (userid,)
        ).fetchone()


@bp.route('/dashboard', methods=('GET', 'POST'))
def dashboard():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (email, username, password) VALUES (?, ?, ?)",
                    (email, username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('event/dashboard.html')


@bp.route('/<int:eventid>', methods=('GET', 'POST'))
def eventid(eventid):
    error = None
    if eventid:
        db = get_db()
        info = db.execute(
            'SELECT * FROM events WHERE eventid = ?', (eventid,)
        ).fetchone()

    else:
        flash('Enter an Event')
        return render_template('schedule.html')

    flash(error)
    return render_template('event/id.html', info=info)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        price = request.form['price']
        desc = request.form['desc']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO events (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, date, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
