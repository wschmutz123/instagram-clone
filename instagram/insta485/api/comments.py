"""REST API for comments."""
import flask
import insta485


@insta485.app.route('/api/v1/p/<int:postid>/comments/',
                    methods=["GET", "POST"])
def get_comment(postid):
    """Return comments on postid."""
    if 'username' not in flask.session:
        message = {
            "message": "Forbidden",
            "status_code": 403
        }
        return flask.jsonify(**message), 403

    connection = insta485.model.get_db()

    check_num_comments = connection.execute(
        "SELECT COUNT(*) as count FROM posts"
    ).fetchone()

    if postid > check_num_comments['count']:
        context = {
            "message": "Not Found",
            "status_code": 404
        }
        return flask.jsonify(**context), 404

    if flask.request.method == "GET":
        comments = connection.execute(
            "SELECT commentid, text, owner, postid "
            "FROM comments WHERE postid = ?", (postid,)
        ).fetchall()

        for comment, _ in enumerate(comments):
            comments[comment]['owner_show_url'] = '/u/'
            comments[comment]['owner_show_url'] += comments[comment]['owner']
            comments[comment]['owner_show_url'] += '/'

        context = {
            "comments": comments,
            "url": flask.request.path,
        }

        return flask.jsonify(**context), 200

    text = flask.request.get_json()
    owner = flask.session['username']

    comments = connection.execute(
        "INSERT INTO comments(owner, postid, text) VALUES(?,?,?) ",
        (owner, str(postid), text['text'])
    )

    inserted_comment = connection.execute(
        """SELECT last_insert_rowid() as id, owner, postid,
            text FROM comments"""
    ).fetchone()

    context = {
        "commentid": inserted_comment['id'],
        "owner": inserted_comment['owner'],
        "owner_show_url": '/u/' + inserted_comment['owner'] + '/',
        "postid": inserted_comment['postid'],
        "text": flask.request.json['text'],
    }
    return flask.jsonify(**context), 201
