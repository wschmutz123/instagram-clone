"""
Insta485 index (main) view.

URLs include:
/u/<username>
"""
import flask
import insta485


@insta485.app.route('/u/<username>/')
def show_user(username):
    """Display /u/<username> route."""
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')

    # Connect to database
    connection = insta485.model.get_db()

    user = connection.execute(
        'SELECT * FROM users WHERE username = ?', (username, )
    ).fetchone()
    # wrong username
    if user is None:
        # return flask.redirect('/accounts/create/')
        flask.abort(404)

    # Query database
    cur = connection.execute(
        "SELECT username1, COUNT(*) AS count "
        "FROM following WHERE username2 = ?", (username,)
    )
    followers = cur.fetchall()

    cur2 = connection.execute(
        "SELECT username2, COUNT(*) AS count "
        "FROM following WHERE username1 = ?", (username,)
    )
    following = cur2.fetchall()

    cur3 = connection.execute(
        "SELECT filename, owner, postid, created, COUNT(*) AS count "
        "FROM posts WHERE owner = ?", (username,)
    )
    num_posts = cur3.fetchall()

    cur4 = connection.execute(
        "SELECT filename, owner, postid, created "
        "FROM posts"
    )

    posts = cur4.fetchall()

    cur5 = connection.execute(
        "SELECT username1, username2 "
        "FROM following"
    )

    cur6 = connection.execute(
        "SELECT fullname "
        f"FROM users WHERE username = '{username}'"
    )

    fullname = cur6.fetchall()

    connection = cur5.fetchall()

    # Add database info to context
    context = {"fullname": fullname, "connection": connection,
               "numPosts": num_posts, "posts": posts, "username": username,
               "following": following, "followers": followers,
               "logname": flask.session['username']}
    return flask.render_template("user.html", **context)
