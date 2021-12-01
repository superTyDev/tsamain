import os
from flask import Flask, request, render_template


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
        return render_template('base.html', file=request, title=(request.split('.')[0]))

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app


if __name__ == "__main__":
    console.log('i ran')
    port = int(os.environ.get('PORT', 33507))
    create_app.run(host='0.0.0.0', port=port)
