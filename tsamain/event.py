import functools
from datetime import datetime
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response, current_app
)
from flask_socketio import join_room, leave_room, send
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.security import check_password_hash, generate_password_hash

from tsamain import socketio
from tsamain.auth import login_required
from tsamain.db import get_db, init_db

bp = Blueprint('event', __name__, url_prefix='/event')


@bp.route('/dashboard', methods=('GET', 'POST'))
@login_required
def dashboard():
    db = get_db()
    error = None
    info = db.execute(
        'SELECT e.eventtitle, e.eventdate, e.eventlevel, e.eventprice, d.eventdesc, d.eventhero, e.eventid, c.cartid FROM cart c LEFT JOIN events e ON c.ceventid = e.eventid LEFT JOIN edetails d ON c.ceventid = d.deventid WHERE (c.cuserid = ? and c.purchased = 1)', (g.user['userid'],)).fetchall()
    db.commit()

    if error is not None:
        flash(error)

    return render_template('event/dashboard.html', info=info)


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


@bp.route('/schedule', methods=('GET', 'POST'))
def schedule():
    if 'num' in request.args:
        num = request.args.get('num')
    else:
        num = 20

    db = get_db()
    info = db.execute('SELECT e.eventtitle, e.eventdate, e.eventlevel, e.eventprice, d.eventdesc, d.eventhero, e.eventid FROM events e LEFT JOIN edetails d ON e.eventid = d.deventid WHERE eventdate > DATE() ORDER BY eventdate ASC LIMIT ?', (num,)).fetchall()
    return render_template('event/schedule.html', info=info)


@bp.route('/<int:eventid>', methods=('GET', 'POST'))
def eventid(eventid):
    request.path = "id"
    error = None
    if eventid:
        db = get_db()
        row = db.execute(
            'SELECT e.eventtitle, e.eventdate, e.eventlevel, e.eventprice, d.eventdesc, d.eventhero FROM events e LEFT JOIN edetails d ON e.eventid = d.deventid WHERE eventid = ?', (
                eventid,)
        ).fetchone()

    else:
        flash('Enter an Event')
        return render_template('schedule.html')

    if error is not None:
        flash(error)
    return render_template('event/id.html', row=row)


@bp.route('/creator', methods=('GET', 'POST'))
@login_required
def creator():
    if g.user["userlevel"] >= 2:
        if request.method == 'POST':
            title = request.form['title']
            date = request.form['date']
            level = request.form.getlist('level')
            price = request.form['price']

            error = None

            if not title:
                error = 'Title is required.'
            elif not date:
                error = 'Date is required.'
            elif not level:
                error = "Select at least one level"
            elif not price:
                error = 'Price is required.'

            level = ", ".join(level)

            if error is not None:
                flash(error)
            else:
                db = get_db()
                cursor = db.execute(
                    'INSERT INTO events (eventtitle, eventdate, eventlevel, eventprice, authorid)'
                    ' VALUES (?, ?, ?, ?, ?)',
                    (title, date, level, price, g.user['userid'])
                )
                db.commit()

                if 'desc' in request.form and request.form['desc'] != "":
                    desc = request.form['desc']
                else:
                    desc = None

                if 'video' in request.files and request.files['video'].filename != "":
                    print(f"-{request.files['video']}-")
                    f = request.files['video']
                    vpath = secure_filename(
                        str(cursor.lastrowid) + "." + f.filename.split(".")[-1])

                    f.save(os.path.join(
                        "tsamain", current_app.config['UPLOAD_FOLDER'], vpath))
                else:
                    vpath = None

                if 'hero' in request.files and request.files['hero'].filename != "":
                    f = request.files['hero']
                    hpath = secure_filename(
                        str(cursor.lastrowid) + "." + f.filename.split(".")[-1])
                    f.save(os.path.join(
                        "tsamain", current_app.config['UPLOAD_FOLDER'], hpath))
                else:
                    hpath = None

                if 'stream' in request.form:
                    slink = request.form['stream']
                else:
                    slink = None

                db.execute(
                    'INSERT INTO edetails (deventid, eventdesc, eventhero, eventvideo, eventstream)'
                    ' VALUES (?, ?, ?, ?, ?)',
                    (cursor.lastrowid, desc, hpath, vpath, slink)
                )
                db.commit()

                flash(f"Event {cursor.lastrowid} created successfully")
                return redirect(url_for('event.dashboard'))
    else:
        flash("No Auth")
        return redirect(url_for('event.dashboard'))

    return render_template('event/create.html')


@ bp.route('/create', methods=('GET', 'POST'))
@ login_required
def create():
    if g.user["userlevel"] >= 2:
        return render_template('event/create.html')
    else:
        flash("No Auth")
        return redirect(url_for('event.dashboard'))


@ bp.route("/room", methods=('GET', 'POST'))
def room():
    return render_template('event/room.html')


@ bp.route("/s", methods=('GET', 'POST'))
def s():
    return render_template('event/s.html')


print("--> init")

rooms = []


@socketio.on('connection')
def on_connect(data):
    print("user connected", data.sid)
    session['curRoom'] = None


@socketio.on('joinRoom')
def on_join(data):
    print("--> join", data.sid)

    if not rooms[data]:
        rooms[data] = {
            name: data,
            occupants: {},
        }

    joinedTime = datatime.datetime.now()
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)


@socketio.on('disconnect')
def on_leave():
    print("--> leave")
