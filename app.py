import os
import re
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/<request>")
def index(request="index.html"):
    if request.find(".") == -1:
        request += ".html"
    return render_template('base.html', file=request, title=(request.split('.')[0]))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
