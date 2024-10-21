"""
Insta485 reditect handling.

URLs include:
/accounts/?target=<url>
"""
import hashlib
import uuid
import pathlib
from flask import render_template, redirect, url_for, request, session
from flask import abort
import insta485


@insta485.app.route("/accounts/", methods=["POST"])
def operation():
    """Operations / route."""
    # treats target as a query
    url = request.args.get("target")
    if url is None:
        url = "/"
    # return url
    oper = request.form["operation"]

    # Login
    if oper == "login":
        login_operation()

    # Create account
    if oper == "create":
        create_operation()

    # Delete account
    if oper == "delete":
        delete_operation()

    # Edit account
    if oper == "edit_account":
        edit_operation()

    # Update password
    if oper == "update_password":
        update_password_operation()

    # test by displaying json of user info
    # users = get_users()
    # return redirect(url_for('test_handle', test=users))
    return redirect(url)


@insta485.app.route("/<test>")
def test_handle(test):
    """Test / route."""
    return test


@insta485.app.route("/accounts/password/", methods=["POST", "GET"])
def update_password():
    """Display / route."""
    # Connect to database
    if "username" not in session:
        abort(403)
    context = {"logname": session['username']}
    return render_template("accounts/password.html", **context)


def calculate_hash(password, tmp):
    """Calculate hash."""
    algorithm = "sha512"
    # if true salt password as normal
    if tmp is None:
        salt = uuid.uuid4().hex
    # else retrieve old salt to validate new password
    else:
        salt = tmp["password"].split("$")[1]

    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode("utf-8"))
    password_hash = hash_obj.hexdigest()
    return "$".join([algorithm, salt, password_hash])


@insta485.app.route("/accounts/edit/", methods=["POST", "GET"])
def edit_account():
    """Display / route."""
    if "username" not in session:
        abort(403)
    connection = insta485.model.get_db()

    user = connection.execute(
        "SELECT * FROM users WHERE username = ?", (session["username"],)
    ).fetchone()

    if request.method == "POST":
        return redirect(url_for("operation"))

    context = {
        "filename": user["filename"],
        "logname": session["username"],
        "fullname": user["fullname"],
        "email": user["email"],
    }
    return render_template("accounts/edit.html", **context)


@insta485.app.route("/accounts/delete/", methods=["POST", "GET"])
def delete_user():
    """Display / route."""
    if "username" not in session:
        abort(403)
    context = {"logname": session['username']}
    return render_template("accounts/delete.html", **context)


@insta485.app.route("/accounts/create/")
def create_account():
    """Display / route."""
    if "username" in session:
        return redirect(url_for("edit_account"))

    return render_template("accounts/create.html")


def get_users():
    """Test / route."""
    conn = insta485.model.get_db()
    cur = conn.cursor()
    users = cur.execute("SELECT * FROM users").fetchall()
    return users


@insta485.app.route("/accounts/logout/", methods=["POST", "GET"])
def logout():
    """Display / route."""
    session.clear()
    return redirect(url_for("login"))


@insta485.app.route("/accounts/login/", methods=["POST", "GET"])
def login():
    """Display / route."""
    if "username" in session:
        return redirect(url_for("show_index"))

    return render_template("/accounts/login.html")


def login_operation():
    """Login function."""
    if request.method == "POST":
        if not request.form["username"] or not request.form["password"]:
            abort(400)
        username = request.form["username"]
        password = request.form["password"]

        connection = insta485.model.get_db()
        user = connection.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        # wrong username
        if user is None:
            abort(403)
        # validate password by salting with original
        password_db_string = calculate_hash(password, user)
        # check validation
        if user["password"] != password_db_string:
            abort(403)

        session["username"] = username


def password_entry(password):
    """Create password in correct format."""
    algorithm = "sha512"
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode("utf-8"))
    password_hash = hash_obj.hexdigest()
    return "$".join([algorithm, salt, password_hash])


def create_operation():
    """Create account operation."""
    username = request.form["username"]
    connection = insta485.model.get_db()

    user = connection.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()

    # Conflict error
    if user is not None:
        abort(409)
    # If any of the fields are empty, abort(400)
    if (
        not request.files["file"]
        or not request.form["fullname"]
        or not request.form["email"]
        or not request.form["password"]
    ):
        abort(400)

    fileobj = request.files["file"]
    fullname = request.form["fullname"]
    email = request.form["email"]
    password = request.form["password"]
    filename = fileobj.filename

    # A password entry in the database contains the algorithm,
    # salt and password hash separated by $. Use the sha512 algorithm:
    password_db_string = password_entry(password)

    # Compute base name (filename without directory). We use a UUID to
    # avoid clashes with existing files and ensure name is compatible
    uuid_basename = "{stem}{suffix}".format(
        stem=uuid.uuid4().hex, suffix=pathlib.Path(filename).suffix
    )

    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
    fileobj.save(path)

    # Insert into database
    sql = """ INSERT INTO users(username, fullname, email, filename,
              password) VALUES(?,?,?,?,?) """
    values = (username, fullname, email, uuid_basename, password_db_string)
    cur = connection.cursor()
    cur.execute(sql, values)
    connection.commit()

    # log the user in
    session["username"] = username


def delete_operation():
    """Delete account function."""
    if 'username' not in session:
        abort(403)

    connection = insta485.model.get_db()
    # Delete the user icon
    tmp = connection.execute(
        "SELECT filename FROM users WHERE username = ?", (session["username"],)
    ).fetchone()
    tmp = tmp["filename"]
    tmp_path = insta485.app.config["UPLOAD_FOLDER"] / pathlib.Path(tmp)
    pathlib.Path.unlink(tmp_path)

    # Delete the the posts from uploads
    tmp = connection.execute(
        "SELECT filename FROM posts WHERE owner = ?", (session["username"],)
    ).fetchall()
    for post in tmp:
        post = post["filename"]
        tmp_path = insta485.app.config["UPLOAD_FOLDER"] / pathlib.Path(post)
        pathlib.Path.unlink(tmp_path)

    # Delete user and all related entries
    connection.execute("DELETE FROM users WHERE username = ?",
                       (session["username"],))
    connection.execute("DELETE FROM posts WHERE owner = ?",
                       (session["username"],))
    connection.execute(
        "DELETE FROM following WHERE username1 = ? OR username2 = ?",
        (
            session["username"],
            session["username"],
        ),
    )
    connection.execute("DELETE FROM comments WHERE owner = ?",
                       (session["username"],))
    connection.execute("DELETE FROM likes WHERE owner = ?",
                       (session["username"],))
    # Clear session and commit
    session.clear()
    connection.commit()


def edit_operation():
    """Edit account function."""
    if 'username' not in session:
        abort(403)

    email = request.form["email"]
    fullname = request.form["fullname"]
    connection = insta485.model.get_db()
    if request.files.get('file', None):
        fileobj = request.files["file"]
        filename = fileobj.filename
        # print(filename)

        # Delete the old file
        tmp = connection.execute(
            "SELECT filename FROM users WHERE username = ?",
            (session["username"],)
        ).fetchone()
        tmp = tmp["filename"]
        tmp_path = insta485.app.config["UPLOAD_FOLDER"] / pathlib.Path(tmp)
        pathlib.Path.unlink(tmp_path)

        # Save to disk
        uuid_basename = "{stem}{suffix}".format(
            stem=uuid.uuid4().hex, suffix=pathlib.Path(filename).suffix
        )
        path = insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
        fileobj.save(path)

        connection.execute(
            "UPDATE users SET fullname = ?, email = ?, filename = ? WHERE "
            " username = ?",
            (fullname, email, uuid_basename, session["username"]),
        )
    else:
        connection.execute(
            "UPDATE users SET fullname = ?, email = ?  WHERE username = ?",
            (fullname, email, session["username"]),
        )


def update_password_operation():
    """Update password function."""
    if 'username' not in session:
        abort(403)

    connection = insta485.model.get_db()
    tmp = connection.execute(
        "SELECT password FROM users WHERE username = ?", (session["username"],)
    ).fetchone()
    # abort if form is unfilled
    if (
        not request.form["password"]
        or not request.form["new_password1"]
        or not request.form["new_password2"]
    ):
        abort(400)

    password = request.form["password"]
    new_password1 = request.form["new_password1"]
    new_password2 = request.form["new_password2"]

    # validate password by salting with original
    password_db_string = calculate_hash(password, tmp)
    # check validation
    if tmp["password"] != password_db_string:
        abort(403)
    # verify new password was entered correctly twice
    if new_password1 != new_password2:
        abort(401)
    # hash new password
    new_password_final = calculate_hash(new_password1, None)
    # update password in the database
    connection.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (
            new_password_final,
            session["username"],
        ),
    )
