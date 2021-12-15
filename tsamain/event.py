import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from tsamain.auth import login_required
from tsamain.db import get_db, init_db

bp = Blueprint('event', __name__, url_prefix='/event')


@bp.route('/dashboard', methods=('GET', 'POST'))
@login_required
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


@bp.route('/initdb')
@login_required
def initdb():
    # error = None
    if g.user["userlevel"] == 3:
        init_db()
        response = "DB Init Began"
    else:
        response = "NO AUTH"

    response = make_response(response, 200)
    response.mimetype = "text/plain"
    return response


@bp.route('/loadevents', methods=('GET', 'POST'))
def loadevents():
    if 'num' in request.args:
        num = request.args.get('num')
    else:
        num = 5

    db = get_db()
    info = db.execute(
        'SELECT * FROM events WHERE eventdate > DATE() ORDER BY eventdate ASC LIMIT ?', (num,)).fetchall()
    return render_template('event/schedule.html', info=info)


@bp.route('/<int:eventid>', methods=('GET', 'POST'))
def eventid(eventid):
    error = None
    if eventid:
        db = get_db()
        info = db.execute(
            'SELECT * FROM events WHERE eventid = ? ', (eventid,)
        ).fetchone()

    else:
        flash('Enter an Event')
        return render_template('schedule.html')

    flash(error)
    return render_template('event/id.html', info=info)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if g.user["userlevel"] >= 2:
        if request.method == 'POST':
            title = request.form['title']
            date = request.form['date']
            level = request.form.getlist('level')
            price = request.form['price']
            desc = request.form['desc']
            error = None

            if not title:
                error = 'Title is required.'
            elif not date:
                error = 'Date is required.'
            elif not level:
                error = "Select at least one level"
            elif not price:
                error = 'Price is required.'
            elif not desc:
                error = 'Description is required.'

            level = " ".join(level)
            print(level)

            if error is not None:
                flash(error)
            else:

                db = get_db()
                db.execute(
                    'INSERT INTO events (eventtitle, eventdate, eventlevel, eventprice, eventdesc, authorid)'
                    ' VALUES (?, ?, ?, ?, ?, ?)',
                    (title, date, level, price, desc, g.user['userid'])
                )
                db.commit()

                return redirect(url_for('event.dashboard'))
    else:
        flash("No Auth")
        return redirect(url_for('event.dashboard'))

    return render_template('event/create.html')
