import os
from flask import Flask, request, render_template
from flask_talisman import Talisman


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'tsamain.sqlite'),
    )

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

    @app.route("/")
    @app.route("/<request>")
    def index(request="index.html"):
        if request.find(".") == -1:
            request += ".html"
        return render_template(request)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    if os.getenv("FLASK_ENV") != "development":
        Talisman(app, content_security_policy=None)

    return app
