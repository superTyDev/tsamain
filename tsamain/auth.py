import functools
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from tsamain.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @ functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please Log In")
            return redirect(url_for('auth.login', next=request.url))
        return view(**kwargs)
    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if 'd' in request.args:
        developer = True
    else:
        developer = False

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        rpassword = request.form['rpassword']

        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        if not username:
            error = 'Username is required.'

        if not password:
            error = 'Password is required.'
        elif password != rpassword:
            error = 'Passwords do not match.'

        if len(password) < 8:
            error = 'Password must be greater than 8 characters'
        if not any(char.isupper() for char in password):
            error = 'Password must have a capital letter'
        if not any(char.isnumeric() for char in password):
            error = 'Password must have a number'

        if not 'userlevel' in request.form:
            userlevel = 1
        else:
            userlevel = request.form['userlevel']

        if not 'credit-number' in request.form:
            creditnumber = None
        else:
            creditnumber = "0000000000000000"

        if error is None:
            try:
                cursor = db.execute(
                    "INSERT INTO user (email, username, password, userlevel) VALUES (?, ?, ?, ?)",
                    (email, username, generate_password_hash(password), userlevel),
                )
                db.execute(
                    "INSERT INTO udetails (duserid, gift, creditcard) VALUES (?, ?, ?)",
                    (cursor.lastrowid, 5, creditnumber),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html', developer=developer)


@ bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        next_url = request.form.get("next")

        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['userid'] = user['userid']
            if next_url:
                return redirect(next_url)
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@ bp.route('/cart', methods=('GET', 'POST'))
@login_required
def cart():
    db = get_db()
    error = None
    info = db.execute(
        'SELECT e.eventtitle, e.eventdate, e.eventlevel, e.eventprice, d.eventdesc, d.eventhero, e.eventid, c.cartid FROM cart c LEFT JOIN events e ON c.ceventid = e.eventid LEFT JOIN edetails d ON c.ceventid = d.deventid WHERE (c.cuserid = ? and c.purchased = 0)', (g.user['userid'],)).fetchall()
    db.commit()

    totalprice = 0
    for row in info:
        totalprice += row['eventprice']

    if error is not None:
        flash(error)

    return render_template('auth/cart.html', info=info, totalprice=totalprice)


@ bp.route('/cartmanage', methods=('GET', 'POST'))
@login_required
def cartmanage():
    if request.method == 'POST':
        error = None

        if 'addcart' in request.form:
            addcart = request.form['addcart']
            db = get_db()
            db.execute(
                'INSERT INTO cart (ceventid, cuserid)'
                ' VALUES (?, ?)',
                (addcart, g.user['userid'])
            )
            db.commit()

        if 'removecart' in request.form:
            removecart = request.form['removecart']
            db = get_db()
            db.execute(
                'DELETE FROM cart WHERE cartid = ?',
                (removecart)
            )
            db.commit()

        if 'purchase' in request.form:
            db = get_db()
            db.execute(
                'UPDATE cart SET purchased = 1 WHERE (cuserid = ? AND purchased = 0)',
                (g.user['userid'],),
            )
            db.commit()

        if error is not None:
            flash(error)

    return redirect(url_for('auth.cart'))


@ bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
