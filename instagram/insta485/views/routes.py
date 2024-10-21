"""
Insta485 index (main) view.

URLs include:
/routes/
"""
import pathlib
import os
import flask
import insta485


@insta485.app.route('/following/', methods=['POST'])
def remove_following():
    """Display / route."""
    url = flask.request.args.get('target')
    if url is None:
        url = '/'
    operation = flask.request.form['operation']
    # Connect to database
    connection = insta485.model.get_db()

    logname = flask.session['username']

    username = flask.request.form['username']

    if operation == 'unfollow':

        cur = connection.execute(
            f"""SELECT COUNT(*) FROM following
            WHERE username1 = '{logname}' AND username2 = '{username}'"""
        )
        result = cur.fetchone()
        count = list(result.values())
        if count[0] == 0:
            flask.abort(409)

        # Removing
        cur = connection.execute(
            f"""DELETE FROM following WHERE username1 = '{logname}'
            AND username2 = '{username}'"""
        )

    else:

        cur = connection.execute(
            f"""SELECT COUNT(*) FROM following WHERE username1 = '{logname}'
            AND username2 = '{username}'"""
        )
        result = cur.fetchone()
        count = list(result.values())
        if count[0] == 1:
            flask.abort(409)
        sql = f"""INSERT INTO following(username1, username2)
        VALUES('{logname}', '{username}')"""

        cur = connection.execute(sql)
    return flask.redirect(url)


@insta485.app.route('/likes/', methods=['POST'])
def likes():
    """Display / route."""
    url = flask.request.args.get('target')
    if url is None:
        url = '/'
    operation = flask.request.form['operation']
    connection = insta485.model.get_db()
    post = flask.request.form['postid']
    logname = flask.session['username']
    if operation == 'unlike':

        cur = connection.execute(
            f"""SELECT COUNT(*) FROM likes WHERE owner = '{logname}'
            AND postid = '{post}'"""
        )
        result = cur.fetchone()
        count = list(result.values())
        if count[0] == 0:
            flask.abort(409)
        cur = connection.execute(
            f"""DELETE FROM likes WHERE owner = '{logname}'
            AND postid = '{post}'"""
        )
    else:

        cur = connection.execute(
            f"""SELECT COUNT(*) FROM likes WHERE owner = '{logname}'
            AND postid = '{post}'"""
        )
        result = cur.fetchone()
        count = list(result.values())
        if count[0] == 1:
            flask.abort(409)
        sql = f"""INSERT INTO likes(owner, postid)
        VALUES('{logname}','{post}')"""
        cur = connection.execute(sql)

    return flask.redirect(url)


@insta485.app.route('/comments/', methods=['POST'])
def comments():
    """Display / route."""
    url = flask.request.args.get('target')
    if url is None:
        url = '/'
    connection = insta485.model.get_db()
    logname = flask.session['username']
    operation = flask.request.form['operation']

    if operation == 'create':
        post = flask.request.form['postid']
        comment = flask.request.form['text']
        if comment.isspace() is True:
            flask.abort(400)
        sql = f"""INSERT INTO comments(owner, postid, text)
        VALUES('{logname}','{post}','{comment}')"""
        cur = connection.execute(sql)
    else:
        commentstring = flask.request.form['commentid']
        cur = connection.execute(
            f"""SELECT COUNT(*) FROM comments WHERE owner = '{logname}'
            AND commentid = '{commentstring}'"""
        )
        result = cur.fetchone()
        count = list(result.values())
        if count[0] == 0:
            flask.abort(403)
        cur = connection.execute(
            f"""DELETE FROM comments WHERE owner = '{logname}'
            AND commentid = '{commentstring}'"""
        )

    return flask.redirect(url)


@insta485.app.route('/posts/', methods=['POST'])
def posts():
    """Display / route."""
    connection = insta485.model.get_db()
    logname = flask.session['username']
    operation = flask.request.form['operation']

    url = flask.request.args.get('target')
    if url is None:
        url = flask.url_for('show_user', username=logname)

    if operation == 'delete':
        post = flask.request.form['postid']
        result = f"SELECT COUNT(*) FROM posts WHERE postid = '{post}' "
        cur = connection.execute(result)
        result = cur.fetchone()
        count = list(result.values())
        if count[0] == 0:
            flask.abort(403)
        # delete jpeg
        tmp = connection.execute(
            f"SELECT owner, filename FROM posts WHERE postid = '{post}'"
        ).fetchone()
        tmp = tmp['filename']
        tmp_path = insta485.app.config['UPLOAD_FOLDER']/tmp
        pathlib.Path.unlink(pathlib.Path(tmp_path))
        # delete comments
        delete_val = f"DELETE FROM comments WHERE postid = '{post}'"
        cur = connection.execute(delete_val)
        # delete likes
        delete_val = f"DELETE FROM likes WHERE postid = '{post}'"
        cur = connection.execute(delete_val)
        # delete post
        sql = f"DELETE FROM posts WHERE postid = '{post}'"
        cur = connection.execute(sql)
    else:
        fileobj = flask.request.files['file']
        filename = fileobj.filename
        if filename == "":
            flask.abort(400)
        path = insta485.app.config["UPLOAD_FOLDER"]
        fileobj.save(os.path.join(path, filename))
        sql = f"""INSERT INTO posts(filename,owner)
        VALUES('{filename}','{logname}')"""
        cur = connection.execute(sql)

    return flask.redirect(url)
