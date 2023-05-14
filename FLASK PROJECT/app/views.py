from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import app, db
from .forms import *
from .models import *


@app.route('/')
def index():
    news_list = News.query.all()
    categories = Category.query.all()
    return render_template('index.html', news=news_list, categories=categories)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/news/<int:news_id>')
@login_required
def news_detail(news_id):
    news = News.query.get(news_id)
    categories = Category.query.all()
    return render_template('news_detail.html', news=news, categories=categories)


@app.route('/create_news', methods=['POST', 'GET'])
@login_required
def create_news():
    form = NewsForm()
    categories = Category.query.all()
    if form.validate_on_submit():
        news = News()
        news.title = form.title.data
        news.text = form.text.data
        news.category_id = form.category.data
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_news.html', form=form, categories=categories)


@app.route('/category/<int:id>')
def news_in_category(id):
    category = Category.query.get(id)
    news = category.news
    category_name = category.title
    categories = Category.query.all()
    return render_template('category.html',
                           news=news,
                           category_name=category_name,
                           categories=categories)


@app.route('/news/edit/<int:news_id>', methods=['GET', 'POST'])
@login_required
def news_edit(news_id):
    form = NewsForm()
    if form.validate_on_submit():
        news = News()
        news.title = form.title.data
        news.text = form.text.data
        # db.session.
        # db.session.add(news)
        # db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_news.html', form=form)
    # return redirect(url_for('create_news'))


@app.route('/news/<int:news_id>/delete')
@login_required
def news_delete(news_id):
    news = News.query.get(news_id)
    db.session.delete(news)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/create_category', methods=['POST', 'GET'])
@login_required
def create_category():
    form = CategoriesForm()
    if form.validate_on_submit():
        category = Category()
        category.title = form.title.data
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_category.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.password = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()

        print('register user')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        # if user and password == user.password:
        if user and check_password_hash(user.password, password):
            login_user(user)

            print('login user')
            return redirect(url_for('index'))
        else:
            # flash('Login or password is not correct')
            print('Login or password is not correct')
            pass

    return render_template('login.html', form=form)


@login_required
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    print('logout user')
    return redirect(url_for('index'))
