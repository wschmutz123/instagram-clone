"""REST API for returnin specific numbers of pages or posts."""
import flask
import insta485


@insta485.app.route('/api/v1/p/', methods=["GET"])
def get_n_results():
    """Get N results."""
    if 'username' not in flask.session:
        cont = {
            "message": "Forbidden",
            "status_code": 403
        }
        return flask.jsonify(**cont), 403

    num_res = flask.request.args.get("size", default=10, type=int)
    num_page = flask.request.args.get("page", default=0, type=int)

    if num_res < 0 or num_page < 0:
        context = {
            "message": "Bad Request",
            "status_code": 400
        }
        return flask.jsonify(**context), 400

    offset = num_res*num_page

    connection = insta485.model.get_db()

    results = connection.execute(
        "SELECT DISTINCT posts.postid FROM posts, following WHERE "
        "(((following.username1 = ?) AND (posts.owner = following.username2)) "
        "OR (posts.owner = ?)) ORDER BY posts.postid DESC LIMIT ? OFFSET ?",
        (flask.session['username'], flask.session['username'],
            str(num_res), str(offset)),
    ).fetchall()

    for post, _ in enumerate(results):
        results[post]['url'] = flask.request.path
        results[post]['url'] += str(results[post]['postid']) + '/'

    next_page = ""

    if len(results) == num_res:
        num_page = num_page + 1
        next_page = flask.request.path + "?size=" + str(num_res)
        next_page += "&page=" + str(num_page)

    context = {
        "next": next_page,
        "results": results,
        "url": flask.request.path,
    }
    return flask.jsonify(**context)
