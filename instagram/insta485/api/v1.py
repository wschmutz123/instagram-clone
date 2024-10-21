"""REST API for services."""
import flask
import insta485


@insta485.app.route('/api/v1/', methods=['GET'])
def services():
    """Return a list of services."""
    context = {
        "posts": "/api/v1/p/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)
