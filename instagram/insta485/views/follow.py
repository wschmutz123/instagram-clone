"""
Insta485 login view.

URLs include:
/followers/
/following/
"""
import flask
import insta485


@insta485.app.route('/u/<path:filename>/following/')
def show_following(filename):
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
    # Connect to database
    connection = insta485.model.get_db()

    user = connection.execute(
        'SELECT * FROM users WHERE username = ?', (filename, )
    ).fetchone()
    # wrong username
    if user is None:
        flask.abort(404)

    # Query database
    cur = connection.execute(
       """SELECT following.username1, following.username2, users.username,
       users.fullname, users.filename
       FROM following LEFT JOIN users
       ON following.username2 = users.username"""

    )

    following = cur.fetchall()

    # Add database info to context
    context = {"following": following, "username": filename,
               "logname": flask.session['username']}
    return flask.render_template("following.html", **context)


@insta485.app.route('/u/<path:filename>/followers/')
def show_followers(filename):
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
    # Connect to database
    connection = insta485.model.get_db()

    user = connection.execute(
        'SELECT * FROM users WHERE username = ?', (filename, )
    ).fetchone()
    # wrong username
    if user is None:
        flask.abort(404)

    # Query database
    cur = connection.execute(
       """SELECT following.username1, following.username2, users.username,
       users.fullname, users.filename
       FROM following LEFT JOIN users
       ON following.username1 = users.username"""
    )

    following = cur.fetchall()

    # Add database info to context
    context = {"following": following, "username": filename,
               "logname": flask.session['username']}
    return flask.render_template("followers.html", **context)
