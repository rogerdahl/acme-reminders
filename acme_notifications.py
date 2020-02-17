#!/usr/bin/env python

import contextlib
import logging
import sqlite3
import sys

import flask
import redis


DEBUG = True

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)
logging.getLogger("slack.web.slack_response").setLevel(logging.INFO)
# noinspection PyArgumentList
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(levelname)-8s %(message)s",
    force=True,
)


app = flask.Flask(__name__)
app.config.from_object("settings")

redis_client = redis.Redis()


@app.before_first_request
def before_first_request():
    pass

@app.before_request
def before_request():
    flask.g.db = connect_db()
    flask.g.db.row_factory = sqlite3.Row
    # By default, sqlite3 forces a disk sync (fsync syscall) after each commit,
    # which is very slow, especially on the RPi. Turning the sync off increases
    # the chance of db corruption but seems unlikely with the rare DB updates
    # performed by this app.
    flask.g.db.execute("PRAGMA synchronous=OFF")


# @app.after_request
# def after_request(response):
#     response.headers.add("Accept-Ranges", "bytes")
#     return response


# @app.teardown_request
# def teardown_request(e):
#     db = getattr(flask.g, 'db', None)
#     if db is not None:
#         db.close()


@app.teardown_appcontext
def close_db(error):
    if hasattr(flask.g, "db"):
        flask.g.db.close()


def connect_db():
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """This can be called manually to create the db if the system doesn't have the sqlite3 command"""
    with contextlib.closing(connect_db()) as db:
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.cli.command("initdb")
def initdb_command():
    init_db()
    print("Initialized the database")


#
# Views.
#


# @app.route("/")
# def index(name=None):
#     return flask.render_template("index.html", name=name)


@app.route('/add', methods=["POST"])
def add_notification():
    title_str = 'title'
    body_str = flask.request.form['msg']
    redis_client.rpush("msg", body_str)
    flask.g.db.execute(
        """
        insert into notifications (title, body)
        values (?, ?);
        """, (title_str, body_str))
    flask.g.db.commit()
    return "ok"


if __name__ == "__main__":
    # Enable profiler
    # from werkzeug.contrib.profiler import ProfilerMiddleware
    # app.config['PROFILE'] = True
    # app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    try:
        app.run(
            host=app.config["HOST_INTERFACE"],
            port=app.config["HOST_PORT"],
            debug=app.config["DEBUG"],
            threaded=True,
        )
    except KeyboardInterrupt:
        sys.exit(0)
