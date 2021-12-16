import functools
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response, current_app
)
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from werkzeug.security import check_password_hash, generate_password_hash

from tsamain.auth import login_required
from tsamain.db import get_db, init_db

bp = Blueprint('event', __name__, url_prefix='/event')


@bp.route('/dashboard', methods=('GET', 'POST'))
@login_required
def dashboard():
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

@bp.route('/schedule', methods=('GET', 'POST'))
def schedule():
    if 'num' in request.args:
        num = request.args.get('num')
    else:
        num = 20

    db = get_db()
    info = db.execute('SELECT e.eventtitle, e.eventdate, e.eventlevel, e.eventprice, d.eventdesc, d.eventhero FROM events e LEFT JOIN details d ON e.eventid = d.deventid WHERE eventdate > DATE() ORDER BY eventdate ASC LIMIT ?', (num,)).fetchall()
    return render_template('event/schedule.html', info=info)


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
                
                if 'desc' in request.form:
                    desc = request.form['desc']
                else:
                    desc = None
                
                if 'video' in request.files:
                    f = request.files['video']
                    vpath = os.path.join("tsamain", current_app.config['UPLOAD_FOLDER'], secure_filename(str(cursor.lastrowid) + "." + f.filename.split(".")[-1]))
                    
                    f.save(vpath)
                else:
                    vpath = None
          
                if 'hero' in request.files:
                    f = request.files['hero']
                    hpath = os.path.join("tsamain", current_app.config['UPLOAD_FOLDER'], secure_filename(str(cursor.lastrowid) + "." + f.filename.split(".")[-1]))                    
                    f.save(hpath)
                else:
                    hpath = None

                if 'stream' in request.form:
                    slink = request.form['stream']
                else:
                    slink = None

                db.execute(
                    'INSERT INTO details (deventid, eventdesc, eventhero, eventvideo, eventstream)'
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
    
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if g.user["userlevel"] >= 2:
        return render_template('event/create.html')
    else:
        flash("No Auth")
        return redirect(url_for('event.dashboard'))
		
    
