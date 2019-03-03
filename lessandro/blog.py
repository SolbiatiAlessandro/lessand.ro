from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from time import ctime

from lessandro.auth import login_required
from lessandro.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db, cursor = get_db()
    cursor.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN users u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )

    # ISSUE: (coming from sqlite -> psql migration) 
    # sqlite was returning dictionaries fetched['key'] = 'value'
    # but psql returns just a list of values, there could some better ways
    # to fix this but this below is just an ugly work around to fix it
    keys = ['id', 'title', 'body', 'created', 'author_id', 'username']
    posts_values  = cursor.fetchall() # this is the list of list of values

    # here I create the list of dicts manually
    posts = []
    for post_values in posts_values:
        post = {keys[i]: post_values[i] for i in range(len(keys))}
        posts.append(post)

    # the dictionary is needed for jinja2 to render template
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None


        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db, cursor = get_db()
            cursor.execute(
                "INSERT INTO post (title, body, created, author_id)"
                " VALUES ('{}', '{}', '{}','{}' )".format(title, body, ctime(),  g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    db, cursor = get_db()
    cursor.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN users u ON p.author_id = u.id"
        " WHERE p.id = '{}'".format(id)
        )

    # this is a copy paste from line 20, should add code reusability
    vals = cursor.fetchone()
    keys = ['id', 'title', 'body', 'created', 'author_id', 'username']
    if vals: post = {keys[i]: vals[i] for i in range(len(keys))}
    else: post = None

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/post')
def post(id):
    post = get_post(id, check_author=False)
    return render_template('blog/post.html', post=post)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db, cursor = get_db()
            cursor.execute(
                "UPDATE post SET title = '{}', body = '{}'"
                " WHERE id = '{}'".format(title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db, cursor = get_db()
    cursor.execute(
            "DELETE FROM post WHERE id = '{}' ".format(id)
                )
    db.commit()
    return redirect(url_for('blog.index'))
