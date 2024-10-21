"""REST API for posts."""
import flask
import insta485


@insta485.app.route('/api/v1/p/<int:postid>/', methods=["GET"])
def get_post(postid):
    """Return post on postid."""
    if 'username' not in flask.session:
        con = {
            "message": "Forbidden",
            "status_code": 403
        }
        return flask.jsonify(**con), 403

    connection = insta485.model.get_db()

    check_num_posts = connection.execute(
        "SELECT COUNT(*) as count FROM posts"
    ).fetchone()

    if postid > check_num_posts['count']:
        con = {
            "message": "Not Found",
            "status_code": 404
        }
        return flask.jsonify(**con), 404

    context = connection.execute(
        "SELECT posts.filename as img_url, posts.owner, posts.created as age, "
        "users.filename AS owner_img_url FROM posts JOIN users ON "
        "users.username = posts.owner WHERE posts.postid = ? "
        "ORDER BY postid DESC", (postid,)
    ).fetchone()

    context['img_url'] = '/uploads/' + context['img_url']
    context['owner_img_url'] = '/uploads/' + context['owner_img_url']
    context['owner_show_url'] = '/u/' + context['owner'] + '/'
    context['post_show_url'] = '/p/' + str(postid) + '/'
    context['url'] = flask.request.path

    return flask.jsonify(**context)
