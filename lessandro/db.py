import click
from flask import current_app, g
from flask.cli import with_appcontext

import os
import psycopg2

# $ heroku pg:pull DATABASE localdb
# $ export DATABASE_URL="dbname='localdb'"

DATABASE_URL = os.environ['DATABASE_URL']


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL)
        g.cursor = g.db.cursor()

    return g.db, g.cursor


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)
    cursor = g.pop('cursor', None)

    if db is not None:
        db.close()
        cursor.close()
        


def init_db():
    """Clear existing data and create new tables."""
    db, cursor = get_db()

    with current_app.open_resource('schema.sql') as f:
        cursor.execute(f.read().decode('utf8'))
        db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
