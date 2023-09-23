import os

import requests as requests
from flask import Flask, render_template, request, redirect, flash, url_for, session
import hashlib
import forms
from models import User, Entry, EntryPh, Chats, Comments, Sub, Likes, MesText
from appl import app, db
from werkzeug.utils import secure_filename

host = "127.0.0.1"
port = 5005

url_redirect = f"http://{host}:{port}/authorization"
app_id = 'c709711868b0605f1cb5'
app_secret = '5af91858f38e09bc6059b7e4e38ba61e45eb2b88'


ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}


# def generate_link(url_redirect):
#     params = dict(client_id=app_id,
#                   redirect_uri=url_redirect,
#                   scope="user",
#                   response_type="code")
#     endpoint = "https://github.com/login/oauth/authorize"
#     response = requests.get(endpoint, params=params)
#
#     return response.url
#
# def get_token_by_code(code, url_redirect):
#     params = dict(client_id=app_id,
#                   client_secret=app_secret,
#                   redirect_uri=url_redirect,
#                   scope= 'user:read',
#                   code=code)
#     headers = {"Accept": "application/json"}
#     endpoint = "https://github.com/login/oauth/access_token"
#     response = requests.post(endpoint, params=params, headers=headers)
#
#     data = response.json()
#     token = data.get("access_token")
#
#     return token
#
# def get_user_info(access_token):
#     # read the GitHub manual about headers
#     headers = {"Authorization": f"token {access_token}"}
#     endpoint = "https://api.github.com/user"
#     response = requests.get(endpoint, headers=headers)
#
#     data = response.json()
#     name = data.get("name")
#     username = data.get("login")
#     email = data.get("email")
#     private_repos_count = data.get("total_private_repos")
#
#     return name, username, email
#
#
# @app.route("/authorization")
# def auth():
#     code = request.args.get("code")
#     token = get_token_by_code(code, url_redirect)
#     name, username, privates = get_user_info(token)
#     return f"<h1> вы {username} авторизованы и у вас {privates} реп :D </h1>"
#
# @app.route("/git_login")
# def git_login():
#     link = generate_link(url_redirect)
#     return redirect(link)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def main_page():
    en = Entry.query.all()
    entry = []
    ph_list = []
    for e in en:
        d = {'id': e.id, 'text': e.text, 'date': e.data, 'photo': None}
        entry.append(d)
        ph = EntryPh.query.filter_by(en_id=e.id).count()
        if ph != 0:
            ph = EntryPh.query.filter_by(en_id=e.id)
            for p in ph:
                ph_list.append(p.photo)
            entry[e.id]['photo'] = ph_list
            ph_list = []

    return render_template("main_page.html")


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            new_key = hashlib.pbkdf2_hmac('sha256', form.password.data.encode('utf-8'), user.salt, 100000)
            if new_key == user.psw:
                session['username'] = user.id
                return redirect(url_for('profile'))
        error = 'Введены неверные данные'
        return render_template("login.html", form=form, error=error)
    return render_template("login.html", form=form)


@app.route("/logout", methods=['GET'])
def logout():
    session['username'] = None
    return redirect(url_for('main_page'))


@app.route('/singup', methods=('GET', 'POST'))
def singup():
    form = forms.SingupForm(request.form)
    if request.method == "POST" and form.validate():
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', form.password.data.encode('utf-8'), salt, 100000)

        user = User(name=form.name.data, email=form.email.data,
                                      psw=key, salt=salt)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template("singup.html", form=form)



@app.route('/profile', methods=('GET', 'POST'))
def profile():
    id = session.get('username')
    if id:
        form = forms.NewEntryForm()
        if form.validate_on_submit():
            entry = Entry(text=form.text.data, us_id=id)
            db.session.add(entry)
            db.session.commit()
            if form.photos:
                print(type(form.photos.data[0]))
                for photo in form.photos.data:
                    en_id = Entry.query.filter_by(text=form.text.data, us_id=id).first()
                    filename = secure_filename(photo.filename)
                    photo.save(app.config['UPLOAD_FOLDER'] + filename)
                    en_ph = EntryPh(photo=filename, en_id=en_id)
                    db.session.add(en_ph)
                    db.session.commit()
        user = User.query.filter_by(id=id).first()
        en = Entry.query.filter_by(us_id=id)
        user = {'name': user.name, 'about': user.about, 'photo': user.photo, 'email': user.email}
        entry = []
        ph_list = []
        for e in en:
            d = {'id': e.id,'text': e.text, 'date': e.data, 'photo': None}
            entry.append(d)
            ph = EntryPh.query.filter_by(en_id=e.id).count()
            if ph != 0:
                ph = EntryPh.query.filter_by(en_id=e.id)
                for p in ph:
                    ph_list.append(p.photo)
                entry[e.id]['photo'] = ph_list
                ph_list = []
        return render_template("profile/profile.html", user=user, form=form, entry=entry)
    else:
        return redirect(url_for('login'))



@app.route('/edit', methods=('GET', 'POST'))
def edit_profile():
    id = session.get('username')
    if id:
        form = forms.EditProfileForms(request.form)
        user = User.query.get(id)
        print(user)
        user_1 = {'id': id, 'name': user.name, 'about': user.about, 'photo': user.photo, 'email': user.email}
        if request.method == "POST" and form.validate():
            user.name = form.name.data
            user.about = form.about.data
            user.email = form.email.data
            user.photo = form.photo.data
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('profile'))

        return render_template("profile/edit_profile.html", form=form, user=user_1)
    else:
        return redirect(url_for('main_page'))

    return render_template("profile/edit_profile.html", form=form)

@app.route("/detete/<int:id>/", methods=('POST', 'GET'))
def delete_prof(id):
    us_id = session.get('username')
    if request.method == "POST":
        if us_id and us_id == id:
            session['username'] = None
            User.query.filter_by(id=id).delete()
            db.session.commit()
        return redirect(url_for('main_page'))
    return render_template("profile/delete.html")



@app.route('/all_chats')
def mes():
    return render_template("chat/all_chats.html")


@app.route('/chat')
def chat():
    return render_template("chat/chat.html")



# @appl.route('/change_psw/<int:id>')
# def change_psw(id):
#     user = User.query.get(id)
#     msg = Message("Feedback", recipients=[user.email])
#     msg.body = "Привет"
#     mail.send(msg)
#     return render_template("change_psw.html")



