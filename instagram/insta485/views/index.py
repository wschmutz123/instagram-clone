"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import arrow
import insta485


@insta485.app.route('/')
def show_index():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')

    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    cur2 = connection.execute(
        "SELECT text, owner, postid "
        "FROM comments"
    )
    comments = cur2.fetchall()

    cur3 = connection.execute(
       "SELECT posts.postid, COUNT(likes.owner) AS count, likes.owner "
       "FROM posts LEFT JOIN likes ON likes.postid = posts.postid "
       "GROUP BY posts.postid"
    )
    likes = cur3.fetchall()

    cur4 = connection.execute(
        "SELECT posts.filename, posts.owner, postid, posts.created, "
        "users.filename AS ownerimage FROM posts JOIN users ON "
        "users.username = posts.owner ORDER BY postid DESC"
    )
    posts = cur4.fetchall()

    cur5 = connection.execute(
        "SELECT following.username1, following.username2 "
        "FROM following WHERE following.username1 = ?",
        (flask.session['username'],)
    )
    following = cur5.fetchall()
    following.append({"username1": flask.session['username'],
                      "username2": flask.session['username']})

    for index, _ in enumerate(posts):
        time = arrow.get(posts[index]['created'])
        timestamp = time.humanize()
        posts[index]['created'] = timestamp
    # Add database info to context
    context = {"posts": posts, "following": following,
               "comments": comments, "likes": likes,
               "logname": flask.session['username']}
    return flask.render_template("index.html", **context)


@insta485.app.route('/uploads/<path:filename>')
def download_file(filename):
    """Display / route."""
    if 'username' not in flask.session:
        flask.abort(403)

    return flask.send_from_directory(insta485.config.UPLOAD_FOLDER, filename,
                                     as_attachment=True)
