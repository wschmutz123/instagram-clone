"""
Insta485 login view.

URLs include:
/explore/
"""
import flask
import insta485


@insta485.app.route('/explore/')
def show_explore():
    """Display / route."""
    # Connect to database
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
    connection = insta485.model.get_db()

    logname = flask.session['username']

    # Query database

    cur2 = connection.execute(
       "SELECT filename, username "
       "FROM users"
    )

    cur3 = connection.execute(
       "SELECT username2 "
       f"FROM following WHERE username1 = '{logname}'"
    )

    following = cur3.fetchall()
    users = cur2.fetchall()

    # Add database info to context
    context = {"following": following, "users": users,
               "logname": flask.session['username']}
    return flask.render_template("explore.html", **context)
