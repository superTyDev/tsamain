import os
from datetime import datetime
import random
from flask import Flask, request, render_template, g, session
from flask_talisman import Talisman
from flask_socketio import SocketIO
from tsamain.db import get_db

socketio = SocketIO(async_mode="threading")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'tsamain.sqlite'),
    )
    app.config['UPLOAD_FOLDER'] = os.path.join("static", "upload")

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.context_processor
    def handle_context():
        return dict(os=os, datetime=datetime, random=random)

    @app.before_request
    def load_logged_in_user():
        userid = session.get('userid')

        if userid is None:
            g.user = None
        else:
            g.user = get_db().execute(
                'SELECT * FROM user WHERE userid = ?', (userid,)
            ).fetchone()

    @app.route("/")
    def index():
        request.path = "index"

        db = get_db()
        info = db.execute('SELECT e.eventtitle, e.eventdate, e.eventlevel, e.eventprice, d.eventdesc, d.eventhero, e.eventid FROM events e LEFT JOIN edetails d ON e.eventid = d.deventid WHERE eventdate > DATE() ORDER BY eventdate ASC LIMIT ?', (10,)).fetchall()

        return render_template("index.html", info=info)

    @app.route("/<request>")
    def main(request):
        return render_template(request + ".html")

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import event
    app.register_blueprint(event.bp)

    if os.getenv("FLASK_ENV") != "development":
        Talisman(app, content_security_policy=None)

    socketio.init_app(app)

    return app
