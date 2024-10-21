"""
Insta485 index (main) view.

URLs include:
/post/
"""
import flask
import arrow
import insta485


@insta485.app.route('/p/<path:post>/')
def show_post(post):
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
    # Connect to database
    connection = insta485.model.get_db()

    user = connection.execute(
        'SELECT * FROM posts WHERE postid = ?', (post, )
    ).fetchone()
    # wrong username
    if user is None:
        flask.abort(404)

    # Query database
    posts = connection.execute(
       "SELECT postid, filename, owner, created "
       "FROM posts"
    ).fetchall()

    comments = connection.execute(
       "SELECT owner, postid, text, created, commentid "
       "FROM comments"
    ).fetchall()

    likes = connection.execute(
       "SELECT owner, postid "
       "FROM likes"
    ).fetchall()

    cur5 = connection.execute(
        "SELECT COUNT(*) AS count "
        f"FROM likes WHERE postid = '{post}'"
    )

    cur4 = connection.execute(
       "SELECT username, filename "
       "FROM users"
    )

    numlikes = cur5.fetchall()
    users = cur4.fetchall()

    for index, _ in enumerate(posts):
        time = arrow.get(posts[index]['created'])
        timestamp = time.humanize()
        posts[index]['created'] = timestamp

#    numlikes = cur5.fetchall()

    # Add database info to context
    context = {"numlikes": numlikes, "posts": posts, "users": users,
               "comments": comments, "likes": likes,
               "logname": flask.session['username'], "postval": int(post)}
    return flask.render_template("post.html", **context)
