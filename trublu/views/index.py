"""
trublu index (main) view.

URLs include:
/
"""
import pathlib
import uuid
import hashlib
import os
from os import path
import flask
from flask import session, redirect, url_for, send_from_directory
import arrow
import trublu


@trublu.app.route('/')
def show_index():
    """Display / route."""
    if 'username' not in session:
        return redirect(url_for('login'))
    print(session['username'])
    # Connect to database
    connection = trublu.model.get_db()

    # Query database
    cur = connection.execute(
        "SELECT * "
        "FROM students"
    )
    students = cur.fetchall()

    return flask.render_template("index.html", **{"students": students})


@trublu.app.route("/uploads/<path:filename>")
def download_file(filename):
    """Get pictures."""
    fname = filename
    if 'username' not in session:
        flask.abort(403)

    filename_to_test = "var/uploads/"

    if not path.exists(filename_to_test + fname):
        flask.abort(404)
    return send_from_directory(trublu.app.config['UPLOAD_FOLDER'], fname)


@trublu.app.route("/users/<users_slug>/", methods=["GET"])
def users_g(users_slug):
    """Get users."""
    if 'username' not in session:
        return flask.redirect(url_for('login'))

    cur = trublu.model.get_db().execute(
        "SELECT *"
        "FROM students"
    )

    students = cur.fetchall()

    student_exists = False
    for student in students:
        if student['username'] == users_slug:
            student_exists = True
    if not student_exists:
        flask.abort(404)

    return flask.render_template("users.html",
                                 **{"users_slug": users_slug,
                                    "students": students})


@trublu.app.route("/tourguides/")
def tourguides():
    """Get followers."""
    if 'username' not in session:
        return flask.redirect(url_for('login'))
    cur = trublu.model.get_db().execute(
        "SELECT * "
        "FROM tourguides"
    )
    tourguides = cur.fetchall()

    context = {"tourguides": tourguides}
    return flask.render_template("tourguides.html", **context)


@trublu.app.route("/tg/<tg_slug>/")
def tg(tg_slug):
    """Get Following."""
    if 'username' not in session:
        return flask.redirect(url_for('login'))
    connection = trublu.model.get_db()

    cur = connection.execute(
        "SELECT * "
        "FROM tourguides"
    )

    tourguides = cur.fetchall()

    final_tg = None

    for tourguide in tourguides:
        if int(tourguide['id']) == int(tg_slug):
            final_tg = tourguide

    if final_tg is None:
        flask.abort(404)

    context = {"tourguide": final_tg}

    return flask.render_template("tg.html", **context)

@trublu.app.route("/become-a-guide/")
def become_a_guide():
    """Get explore."""
    if 'username' not in session:
        return redirect(url_for('login'))

    return flask.render_template("become.html")


@trublu.app.route("/match/")
def match():
    if 'username' not in session:
        return redirect(url_for('login'))

    return flask.render_template("match.html")



@trublu.app.route("/accounts/login/", methods=["GET"])
def login():
    """Get Login."""
    if 'username' in session:
        return flask.redirect(url_for('show_index'))
    return flask.render_template("login.html")


@trublu.app.route("/accounts/logout/", methods=["POST"])
def logout():
    """Get logout."""
    flask.session.clear()
    return flask.redirect(flask.url_for("login"))


@trublu.app.route("/accounts/create/", methods=["GET"])
def accounts_create():
    """Get Accounts Create."""
    if 'username' in session:
        return flask.render_template(url_for('accounts_edit'))
    return flask.render_template("create.html")


@trublu.app.route("/accounts/delete/")
def accounts_delete():
    """Get Accounts Delete."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return flask.render_template("delete.html")


@trublu.app.route("/accounts/edit/")
def accounts_edit():
    """Get Accounts edit."""
    connection = trublu.model.get_db()
    cur = connection.execute(
        "SELECT *"
        "FROM students"
    )
    students = cur.fetchall()
    for student in students:
        if student["username"] == session["username"]:
            context = {"student": student}

    return flask.render_template("edit.html", **context)


@trublu.app.route("/accounts/password/")
def accounts_password():
    """Get Accounts password."""
    return flask.render_template("password.html")


@trublu.app.route("/mytourguides/", methods=["POST"])
def post_mytourguides():
    if 'username' not in session:
        return redirect(url_for('login'))
    connection = trublu.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM tourguides"
    )
    tourguides = cur.fetchall()
    max_score = 0
    state = flask.request.form.get('state')
    #need correct value from form
    print(state)
    school = flask.request.form.get('school')
    major1 = flask.request.form.get('major1')
    major2 = flask.request.form.get('major2')
    ec1 = flask.request.form.get('ec1')
    ec2 = flask.request.form.get('ec2')
    ec3 = flask.request.form.get('ec3')
    scores = {}
    for guide in tourguides:

        scores[guide["id"]] = 0
        print(guide["firstname"])
        if state == "in" and guide["state"] == "MI":
            scores[guide["id"]] += 1
            print("instate")
        if state == "out" and guide["state"] != "MI":
            scores[guide["id"]] += 1
            print("outstate")
        if school == guide["college"]:
            scores[guide["id"]] += 1
            print("shcool")
        if major1 == guide["majorone"] or major1 == guide["majortwo"] or major1 == guide["majorthree"]:
            scores[guide["id"]] += 3
            print("major")
        if major2 == guide["majorone"] or major2 == guide["majortwo"] or major2 == guide["majorthree"]:
            scores[guide["id"]] += 3
            print("major")
        if (ec1 == guide["econe"] or ec1 == guide["ectwo"] or ec1 == guide["ecthree"] or
        ec1 == guide["ecfour"] or ec1 == guide["ecfive"]):
            scores[guide["id"]] += 2
            print("ec1")
        if (ec2 == guide["econe"] or ec2 == guide["ectwo"] or ec2 == guide["ecthree"] or
        ec2 == guide["ecfour"] or ec2 == guide["ecfive"]):
            scores[guide["id"]] += 2
            print("ec2")
        if (ec3 == guide["econe"] or ec3 == guide["ectwo"] or ec3 == guide["ecthree"] or
        ec3 == guide["ecfour"] or ec3 == guide["ecfive"]):
            scores[guide["id"]] += 2
            print("ec3")
    scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    print(scores)
    top3 = {k: scores[k] for k in list(scores)[:3]}
    top3 = list(top3)
    print(top3)
    context = {"first" : tourguides[top3[0]-1],
               "second" : tourguides[top3[1]-1],
               "third" : tourguides[top3[2]-1]}
    return flask.render_template("mytourguides.html", **context)

@trublu.app.route("/accounts/", methods=["POST"])
def accounts():
    """Post accounts."""
    if flask.request.form["operation"] == "students":
        firstname = flask.request.form["firstname"]
        lastname = flask.request.form['lastname']
        trublu.model.get_db().execute(
            "INSERT INTO students"
            "(firstname, lastname) "
            "VALUES(?, ?)",
            (firstname, lastname)
        )
        trublu.model.get_db().commit()

    if flask.request.form["operation"] == "login":
        username = flask.request.form['username']
        txt_pw = flask.request.form['password']
        target = flask.request.args.get('target')
        print("here")
        print(target)
        if username == "" or txt_pw == "":
            flask.abort(400)
        error = post_login(username, txt_pw)
    if flask.request.form["operation"] == "create":
        if 'username' in session:
            return flask.redirect(url_for("show_index"))
        username = flask.request.form["username"]
        pw_txt = flask.request.form['password']
        firstname = flask.request.form["firstname"]
        lastname = flask.request.form["lastname"]
        email = flask.request.form["email"]
        phonenumber = flask.request.form['phonenumber']
        return post_create(username, pw_txt, firstname, lastname, email, phonenumber)
    if 'username' not in session:
        return flask.render_template("login.html", **{"error": error})
    if flask.request.form["operation"] == "delete":
        username_to_delete = flask.session['username']
        target = flask.request.args.get('target')
        return post_delete(username_to_delete, target)
    if flask.request.form["operation"] == "edit_account":
        firstname = flask.request.form["firstname"]
        lastname = flask.request.form["lastname"]
        email = flask.request.form["email"]
        phonenumber = flask.request.form["phonenumber"]
        target = flask.request.args.get('target')
        return post_edit_account(firstname, lastname, email, phonenumber, target)
    if flask.request.form["operation"] == "update_password":
        txt_new_pw1 = flask.request.form["new_password1"]
        txt_new_pw2 = flask.request.form["new_password2"]
        txt_pw = flask.request.form["password"]
        target = flask.request.args.get('target')
        return post_update_password(txt_new_pw1, txt_new_pw2, txt_pw, target)
    print("end of accounts post")
    return flask.redirect(url_for('show_index'))


def post_login(username, txt_pw):
    """Post login."""
    cur = trublu.model.get_db().execute(
        "SELECT * "
        "FROM students"
    )
    students = cur.fetchall()
    student_found = False
    hashed_password = ""
    for student in students:
        if student['username'] == username:
            student_found = True
            hashed_password = student['password']
            print(hashed_password)

    valid_login = False
    if student_found:
        salt_split = hashed_password.split("$")
        print(salt_split)
        salt = salt_split[1]
        algorithm = 'sha512'
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + txt_pw
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])
        if hashed_password == password_db_string:
            valid_login = True
        else:
            error = "Incorrect Password"
            return error
    else:
        print("here1")
        # flask.render_template("followers.html", **context)
        # return flask.render_template("login.html", **{"error": "Account Does Not Exist"})
        # return flask.redirect(url_for("show_index"))
        error = "Account Does Not Exist"
        return error

    flask.session["username"] = username
    return


def post_create(username, pw_txt, firstname, lastname, email, phonenumber):
    """Post create."""
    cur = trublu.model.get_db().execute(
        "SELECT * "
        "FROM students"
    )
    students = cur.fetchall()
    for student in students:
        if student['username'] == username:
            flask.abort(409)

    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + pw_txt
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_str = "$".join([algorithm, salt, password_hash])

    trublu.model.get_db().execute(
        "INSERT INTO students"
        "(username, firstname, lastname, email, phonenumber, password) "
        "VALUES(?, ?, ?, ?, ?, ?)",
        (username, firstname, lastname, email, phonenumber, password_db_str)
    )

    trublu.model.get_db().commit()

    flask.session["username"] = username

    return flask.redirect(url_for("show_index"))


def post_delete(username_to_delete, target):
    """Post delete."""
    connection = trublu.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM students"
    )
    students = cur.fetchall()
    for student in students:
        if session['username'] == student['username']:
            firstname = student['firstname']
    connection.execute(
        "DELETE FROM students WHERE username = (?) AND firstname = (?)",
        (username_to_delete, firstname)
    )
    connection.commit()
    flask.session.clear()
    if target is None:
        return flask.redirect(url_for('show_index'))
    return flask.redirect(target)


def post_edit_account(firstname, lastname, email, phonenumber, target):
    """Post edit account."""
    connection = trublu.model.get_db()

    connection.execute(
        "UPDATE students SET firstname = (?), lastname = (?), email = (?), phonenumber = (?) "
        "WHERE username = (?)",
        (firstname, lastname, email, phonenumber, session['username'])
    )
    connection.commit()

    return flask.redirect(target)


def post_update_password(txt_new_pw1, txt_new_pw2, txt_pw, target):
    """Post update password."""
    cur = trublu.model.get_db().execute(
        "SELECT * "
        "FROM students"
    )
    students = cur.fetchall()
    for student in students:
        if student['username'] == session["username"]:
            hashed_password = student['password']
    if str(txt_pw) == "" or str(txt_new_pw1) == "":
        flask.abort(400)
    if str(txt_new_pw2) == "":
        flask.abort(400)
    salt_split = hashed_password.split("$")
    salt = salt_split[1]
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + txt_pw
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    if hashed_password != password_db_string:
        return flask.redirect(url_for("accounts_password"))
        # flask.render_template("password.html", **{"error": "Incorrect Password"})
    if str(txt_new_pw1) != str(txt_new_pw2):
        # flask.render_template("password.html", **{"error": "New Passwords Do Not Match"})
        # flash('You were successfully logged in')
        # flask.redirect(url_for("accounts_password"))
        return flask.redirect(url_for("accounts_password"))
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + txt_new_pw1
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    trublu.model.get_db().execute(
        "UPDATE students SET password = (?) WHERE username = (?)",
        (password_db_string, session['username'])
    )
    trublu.model.get_db().commit()
    return flask.redirect(target)
