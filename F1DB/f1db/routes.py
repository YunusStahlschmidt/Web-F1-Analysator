import os
import secrets
from PIL import Image
from datetime import datetime, timezone
from flask import render_template, redirect, flash, url_for, request, abort, jsonify
from F1DB.f1db.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, QueryForm
from F1DB.f1db import app, bcrypt, db, cursor
from flask_login import login_user, current_user, logout_user, login_required
from F1DB.f1db.models import User, Post, logged_in_user, Result
from F1DB.f1db.queries import race_and_results_queries, form_list
from flask_paginate import Pagination, get_page_args


@app.route('/')
@app.route('/home')
def home():
    cursor.execute("select * from posts")
    results = cursor.fetchall()
    posts = []
    for p in results:
        post = Post(p[0], p[1], p[2], p[3], p[4])
        posts.append(post)
    posts.sort(key=lambda post: post.date_posted, reverse=True)
    return render_template("home.html", posts=posts)


@app.route("/query", methods=["POST", "GET"])
def query():
    form = QueryForm()
    form.round.choices = [("All", "All")]
    form.res_per.data = 30
    form.page.data = 1
    if request.method == "POST":
        if len(form_list) == 1:
            form_list.pop()
        form_list.append(form)
        return redirect(url_for("results"))
    return render_template("query.html", title='Query DB', form=form)


@app.route("/results")
def results():
    table, result, headers = race_and_results_queries()
    res = Result(table, result, headers)
    num_rows = len(headers)
    last_col = num_rows - 1
    return render_template("results.html", title='Results', result=res, num_rows=num_rows, last_col=last_col)


@app.route("/round/<season>")
def season(season):
    init_res = [("All",)]
    if season == "All":
        init_res = init_res
    elif season == "Current":
        s = datetime.now()
        season = s.year
        cursor.execute(f"select round from races where year={int(season)}")
        res = cursor.fetchall()
        init_res += res
    else:
        cursor.execute(f"select round from races where year={int(season)}")
        res = cursor.fetchall()
        init_res += res
    rounds = [(str(r[0]), str(r[0])) for r in init_res]
    return jsonify({"rounds": rounds})


@app.route("/predict",  methods=["POST", "GET"])
@login_required
def predict():
    return render_template("predict.html", title='Predict')


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_name = form.username.data
        user_email = form.email.data
        user_password = hashed_password
        cursor.execute("insert into users(user_name, user_email, user_password)"
                       "values(%s,%s,%s)", (user_name, user_email, user_password))
        db.commit()
        flash('Your account has been created! You are able to log in now.', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        cursor.execute(f"select * from users where user_email = '{form.email.data}'")
        user_data = cursor.fetchone()
        user = User()
        user.id, user.username, user.email, user.password, user.type, user.points_of_week, user.week, user.image_file \
            = user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[7]
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            logged_in_user.append(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    logged_in_user.pop(0)
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static\profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail = output_size
    i.save(picture_path)
    cursor.execute(f"update users set user_img='{picture_fn}' where user_id='{logged_in_user[0].id}'")
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            logged_in_user[0].image_file = picture_file
        logged_in_user[0].username = form.username.data
        logged_in_user[0].email = form.email.data
        #     current_user.image_file = picture_file
        # current_user.username = form.username.data
        # current_user.email = form.email.data
        cursor.execute(f"update users set user_name='{logged_in_user[0].username}', user_email='{logged_in_user[0].email}' where user_id='{logged_in_user[0].id}'")
        # cursor.execute("update users set user_name=%s, user_email=%s where user_id=%s",
        #                (current_user.username, current_user.email, current_user.id))
        db.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = logged_in_user[0].username
        form.email.data = logged_in_user[0].email
        # form.username.data = current_user.username
        # form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + logged_in_user[0].image_file)
    # image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html', title='Account', image_file=image_file, form=form)


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        cursor.execute("insert into posts(post_title, post_date, post_content, user_id)" 
                       "values(%s,%s,%s,%s)", (form.title.data, utc_to_local(datetime.utcnow()), form.content.data, current_user.id))
        db.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='Create Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    cursor.execute(f"select * from posts where post_id='{post_id}'")
    p = cursor.fetchone()
    if p is not None:
        post = Post(p[0], p[1], p[2], p[3], p[4])
        return render_template('post.html', title=post.title, post=post)
    else:
        abort(404)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    cursor.execute("select * from posts where post_id=%s", (post_id,))
    p = cursor.fetchone()
    if p is not None:
        if p[4] != current_user.id:
            abort(403)
        form = PostForm()
        if form.validate_on_submit():
            cursor.execute(f"update posts set post_title='{form.title.data}', post_content='{form.content.data}' where post_id='{p[0]}'")
            db.commit()
            flash('Your post has been updated!', 'success')
            return redirect(url_for('post', post_id=p[0]))
        elif request.method == 'GET':
            form.title.data = p[1]
            form.content.data = p[3]
        return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')
    else:
        abort(404)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    cursor.execute(f"select * from posts where post_id='{post_id}'")
    p = cursor.fetchone()
    if p is not None:
        if p[4] != current_user.id:
            abort(403)
        cursor.execute(f"delete from posts where post_id='{p[0]}'")
        db.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(url_for('home'))
