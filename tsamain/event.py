import re
import time
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response, current_app
)
from flask_socketio import join_room, leave_room, send
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

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
        "SELECT e.eventtitle, e.eventdate, e.eventlevel, e.eventprice, d.eventdesc, d.eventhero, e.eventid, c.cartid FROM cart c LEFT JOIN events e ON c.ceventid = e.eventid LEFT JOIN edetails d ON c.ceventid = d.deventid WHERE (c.cuserid = ? and c.purchased = 1) AND eventdate > DATE('now', '-2 hours') ORDER BY eventdate ASC", (g.user['userid'],)).fetchall()
    made = db.execute(
        "SELECT e.eventtitle, e.eventdate, e.eventlevel, e.eventprice, d.eventdesc, d.eventhero, e.eventid FROM events e LEFT JOIN edetails d ON e.eventid = d.deventid WHERE (e.authorid = ?) AND eventdate > DATE('now', '-2 hours') ORDER BY eventdate ASC ", (g.user['userid'],)).fetchall()
    db.commit()

    if error is not None:
        flash(error)

    return render_template('event/dashboard.html', info=info, made=made)


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
    clause = ""
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM events e WHERE eventdate > DATE('now', '-2 hours') " +
                       clause, ()).fetchall()

    if 'a' in request.args and request.args.get('a') != "":
        clause += " AND u.username LIKE '%" + \
            re.sub(r'\W+', '', request.args.get('a')) + "%'"
        author = request.args.get('a')
    else:
        author = ""

    if 'r' in request.args and request.args.get('r') != "" and int(request.args.get('r')) < count[0][0]:
        num = request.args.get('r')
    else:
        num = 0

    if 'q' in request.args and request.args.get('q') != "":
        clause += " AND e.eventtitle LIKE '%" + \
            re.sub(r'\W+', '', request.args.get('q')) + "%'"
        query = request.args.get('q')
    else:
        query = ""

    info = db.execute("SELECT e.eventtitle, e.eventdate, e.eventlevel, e.eventprice, d.eventdesc, d.eventhero, e.eventid FROM events e LEFT JOIN edetails d ON e.eventid = d.deventid LEFT JOIN user u ON u.userid = e.authorid WHERE eventdate > DATE('now', '-2 hours') " +
                      clause + " ORDER BY eventdate ASC LIMIT ?, 10", (num,)).fetchall()
    return render_template('event/schedule.html', info=info, count=count[0][0], num=num, author=author, query=query)


@ bp.route('/live/<int:eventid>', methods=('GET', 'POST'))
def eventroom(eventid):
    request.path = "live"

    error = None
    if eventid:
        db = get_db()
        row = db.execute(
            'SELECT e.eventtitle, e.eventdate, e.eventlevel, e.eventprice, d.eventdesc, d.eventhero, d.eventvideo FROM events e LEFT JOIN edetails d ON e.eventid = d.deventid WHERE eventid = ?', (
                eventid,)
        ).fetchone()
        if g.user != None:
            name = g.user['username']
        else:
            name = time.time()

        if "iframe" in request.args:
            return render_template('event/scene.html', eventid=eventid, row=row, name=name)
        else:
            return render_template("event/room.html", eventid=eventid, row=row, name=name)


@ bp.route('/<int:eventid>', methods=('GET', 'POST'))
def eventid(eventid):
    request.path = "id"
    error = None
    if eventid:
        db = get_db()
        row = db.execute(
            'SELECT e.eventtitle, e.eventdate, e.eventlevel, e.eventprice, d.eventdesc, d.eventhero, u.username, u.userid FROM events e LEFT JOIN edetails d ON e.eventid = d.deventid LEFT JOIN user u ON u.userid = e.authorid WHERE eventid = ?', (
                eventid,)
        ).fetchone()

    else:
        flash('Enter an Event')
        return render_template('event/schedule.html')

    if error is not None:
        flash(error)
    return render_template('event/id.html', row=row)


@ bp.route('/creator', methods=('GET', 'POST'))
@ login_required
def creator():
    if g.user["userlevel"] >= 2:
        if request.method == 'POST':
            if 'removeevent' in request.form:
                removeevent = request.form['removeevent']
                db = get_db()
                db.execute(
                    'DELETE FROM events WHERE eventid = ?',
                    (removeevent,)
                )
                db.commit()
                flash(f'Event {removeevent} was deleted.')
                return redirect(url_for('event.dashboard'))

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


print("--> init")
rooms = {}


@ socketio.on('connection')
def on_connect(data):
    print("\n\n--> connect")


@ socketio.on('joinRoom')
def on_join(data):
    print("\n\n--> join", request.sid)
    room = data['room']

    if not room in rooms:
        rooms[room] = {
            "name": room,
            "occupants": {},
        }

    joinedTime = int(time.time())
    rooms[room]["occupants"][request.sid] = joinedTime
    session['curRoom'] = room

    print(f"{request.sid} joined room {room}")
    join_room(room)

    socketio.emit("connectSuccess", {"joinedTime": joinedTime})
    occupants = {"occupants": rooms[room]["occupants"]}
    print(occupants)
    socketio.emit("occupantsChanged", occupants, room=room)


@ socketio.on("send")
def send(data):
    socketio.emit("send", data, to=data["to"])


@ socketio.on("broadcast")
def broadcast(data):
    socketio.emit("broadcast", data,
                  room=session['curRoom'], broadcast=True)


@ socketio.on('disconnect')
def on_leave():
    print("\n\n--> leave")
    if (rooms[session['curRoom']]):
        print("user disconnected", request.sid)

        del rooms[session['curRoom']]['occupants'][request.sid]
        occupants = {"occupants": rooms[session['curRoom']]['occupants']}
        socketio.emit("occupantsChanged", occupants, room=session['curRoom'])

        if not occupants:
            print("everybody left room")
            del rooms[session['curRoom']]
