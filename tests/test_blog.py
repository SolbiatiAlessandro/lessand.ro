import pytest
from lessandro.db import get_db


def test_index(client, auth):
    response = client.get('/')
    # I don't want LogIn to be shown in main page
    # assert b"Log In" in response.data
    # assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    #assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test body' in response.data
    assert b'href="/1/update"' in response.data

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db, cursor = get_db()
        cursor.execute(
                'UPDATE post SET author_id = 2 WHERE id = 1'
                )
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404

def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200

    with app.app_context():
        db, cursor = get_db()
        cursor.execute(
                'SELECT COUNT(id) FROM post'
                )
        before_count = cursor.fetchone()[0]

        client.post('/create', data={'title': 'created', 'body': ''})

        cursor.execute(
                'SELECT COUNT(id) FROM post'
                )
        count = cursor.fetchone()[0]
        assert count - before_count == 1

def test_create_special_char(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    with app.app_context():
        db, cursor = get_db()
        cursor.execute(
                'SELECT COUNT(id) FROM post'
                )
        before_count = cursor.fetchone()[0]

        client.post('/create', data={'title': 'special_char1', 'body': 'standard chars'})
        client.post('/create', data={'title': 'special_char1', 'body': 'standard chars ) ( + / x % < >'})
        client.post('/create', data={'title': 'special_char1', 'body': "standard chars ' "})

        cursor.execute(
                'SELECT COUNT(id) FROM post'
                )
        count = cursor.fetchone()[0]

        assert count - before_count == 3


def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    with app.app_context():
        db, cursor = get_db()
        cursor.execute(
                'SELECT * FROM post WHERE id = 1'
                )
        vals = cursor.fetchone()
        keys = ['id', 'author_id', 'created', 'title', 'body']
        assert len(vals) == len(keys)

        if vals: post = {keys[i]: vals[i] for i in xrange(len(keys))}
        else: post = None
        assert post['title'] == 'updated'

def test_post(client, auth, app):
    # test without login
    with app.app_context():
        db, cursor = get_db()
        cursor.execute('SELECT * FROM post;')
        vals = cursor.fetchone()
        keys = ['id', 'author_id', 'created', 'title', 'body']
        if vals: post = {keys[i]: vals[i] for i in xrange(len(keys))}

        response =  client.get('/'+str(post['id'])+'/post')
        assert response.status_code == 200
        assert post['title'] in response.data

    # test with login
    auth.login()
    with app.app_context():
        db, cursor = get_db()
        cursor.execute('SELECT * FROM post;')
        vals = cursor.fetchone()
        keys = ['id', 'author_id', 'created', 'title', 'body']
        if vals: post = {keys[i]: vals[i] for i in xrange(len(keys))}

        response =  client.get('/'+str(post['id'])+'/post')
        assert response.status_code == 200
        assert post['title'] in response.data
        assert post['body'] in response.data



@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data

def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        db, cursor = get_db()
        cursor.execute(
                'SELECT * FROM post WHERE id = 1'
                )
        post= cursor.fetchone()
        assert post is None
