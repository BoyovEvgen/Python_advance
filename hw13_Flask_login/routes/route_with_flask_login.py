from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import func
from app import app, db, manager
from models import User, Post, Comment



@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        if not (email or password):
            flash('Fill email and password fields')
        hash_pwd = generate_password_hash(password)
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hash_pwd)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('hello_world'))

    return render_template("sign-up.html")


@app.route("/sign-in", methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        print(request.method)
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('successfully login')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('hello_world'))
            flash('login or password is not correct')
            return render_template("sign-in.html")
        flash('Fill email and password fields')
    return render_template("sign-in.html")


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('sign_in') + '?next=' + request.url)

    return response


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/blog', methods=['GET'])
def blog():
    # posts = Post.query.all()
    # sorted_posts = sorted(posts, key=lambda p: p.datetime, reverse=True)
    sorted_posts = Post.query.order_by(Post.datetime.desc()).all()
    return render_template('blog.html', posts=sorted_posts)


@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        message = request.form.get('message')
        title = request.form.get('title')
        new_post = Post(text=message, title=title, autor=current_user.get_id())
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog'))
    return render_template('add_post.html')


@app.route('/add-comment', methods=['POST'])
@login_required
def add_comment():
    message = request.form.get('message')
    post_id = request.form.get('post_id')

    new_comment = Comment(text=message, autor=current_user.get_id(), post=post_id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('blog'))


@app.route('/change-post', methods=['GET', 'POST'])
@login_required
def change_post():
    if request.method == 'GET':
        post_id = request.args.get('post')
        post = Post.query.get(post_id)
        if current_user.get_id() == str(post.autor):
            return render_template('change-post.html', post=post)
        else:
            flash('You have no access')
            return redirect(url_for('blog'))
    if request.method == 'POST':
        post_id = request.form.get('post_id')
        message = request.form.get('message')
        title = request.form.get('title')
        post = Post.query.get(post_id)
        if current_user.get_id() == str(post.autor):
            post.text = message
            post.title = title
            db.session.commit()
            return redirect(url_for('blog'))
        else:
            flash('You have no access')
            return redirect(url_for('blog'))


@app.route('/del-post')
@login_required
def del_post():
    post_id = request.args.get('post')
    post = Post.query.get(post_id)
    if current_user.get_id() == str(post.autor):
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('blog'))
    flash('You have no access')
    return redirect(url_for('blog'))


@app.route('/search', methods=['POST'])
def search():
    search_title = request.form.get('search')
    search_query = f'%{search_title}%'
    filter_sorted_posts = Post.query.filter(func.lower(Post.title).like(func.lower(search_query))).all()
    return render_template('blog.html', posts=filter_sorted_posts)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
