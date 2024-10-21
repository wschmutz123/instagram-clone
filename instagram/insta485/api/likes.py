"""REST API for likes."""
import flask
import insta485


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/', methods=["GET"])
def get_likes(postid_url_slug):
    """Return post on postid."""
    if 'username' not in flask.session:
        error = {
            "message": "Forbidden",
            "status_code": 403
        }
        return flask.jsonify(**error), 403

    postid = int(postid_url_slug)
    logname = flask.session['username']
    connection = insta485.model.get_db()

    test = f"""SELECT COUNT(*) AS count
    FROM posts WHERE postid = '{postid}'"""
    cur = connection.execute(test)
    check_postid = cur.fetchone()
    count = check_postid['count']
    if count == 0:
        error = {
            "message": "Not Found",
            "status_code": 404
        }
        return flask.jsonify(**error), 404

    select_likes = f"""SELECT COUNT(*) AS count
    FROM likes WHERE owner = '{logname}' AND postid = '{postid_url_slug}'"""
    cur = connection.execute(select_likes)
    logname_likes = cur.fetchone()
    logname_likes_this = logname_likes['count']
    total_likes = f"""SELECT COUNT(*) AS count
    FROM likes WHERE postid = '{postid_url_slug}'"""
    cur = connection.execute(total_likes)
    total_likes = cur.fetchone()
    likes_count = total_likes['count']
    context = {
        "logname_likes_this": logname_likes_this,
        "likes_count": likes_count,
        "postid": postid,
        "url": flask.request.path,
    }
    return flask.jsonify(**context)


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/',
                    methods=["DELETE"])
def delete_likes(postid_url_slug):
    """Return post on postid."""
    if 'username' not in flask.session:
        contexts = {
            "message": "Forbidden",
            "status_code": 403
        }
        return flask.jsonify(**contexts), 403

    postid = int(postid_url_slug)
    logname = flask.session['username']
    connection = insta485.model.get_db()

    test = f"""SELECT COUNT(*) AS count
    FROM posts WHERE postid = '{postid}'"""
    cur = connection.execute(test)
    check_postid = cur.fetchone()
    count = check_postid['count']
    if count == 0:
        contexts = {
            "message": "Not Found",
            "status_code": 404
        }
        return flask.jsonify(**contexts), 404

    logname = flask.session['username']
    connection = insta485.model.get_db()
    del_likes = f"""DELETE FROM likes
    WHERE owner = '{logname}' AND postid = '{postid_url_slug}'"""
    cur = connection.execute(del_likes)
    response = flask.make_response('', 204)
    response.mimetype = insta485.app.config['JSONIFY_MIMETYPE']
    return response


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/', methods=["POST"])
def create_likes(postid_url_slug):
    """Return post on postid."""
    if 'username' not in flask.session:
        error = {
            "message": "Forbidden",
            "status_code": 403
        }
        return flask.jsonify(**error), 403

    postid = int(postid_url_slug)
    logname = flask.session['username']
    connection = insta485.model.get_db()

    test = f"""SELECT COUNT(*) AS count
    FROM posts WHERE postid = '{postid}'"""
    cur = connection.execute(test)
    check_postid = cur.fetchone()
    count = check_postid['count']
    if count == 0:
        error = {
            "message": "Not Found",
            "status_code": 404
        }
        return flask.jsonify(**error), 404

    cur = connection.execute(
        f"""SELECT COUNT(*) FROM likes WHERE owner = '{logname}'
        AND postid = '{postid}'"""
    )
    result = cur.fetchone()
    count = list(result.values())
    if count[0] == 1:
        context = {
            "logname": logname,
            "message": "Conflict",
            "postid": postid,
            "status_code": 409
        }
        return flask.jsonify(**context), 409
    sql = f"""INSERT INTO likes(owner, postid)
    VALUES('{logname}','{postid}')"""
    cur = connection.execute(sql)
    context = {
        "logname": logname,
        "postid": postid,
    }
    return flask.jsonify(**context), 201
