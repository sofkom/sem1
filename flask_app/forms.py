from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, MultipleFileField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[Email(message='Неправильный email'), DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")

class SingupForm(FlaskForm):
    name = StringField('Имя пользователя', validators = [DataRequired(), Length(min=4, max=25)])
    email = StringField("Email",validators=[Email(message='Неправильный email'), DataRequired()])
    password = PasswordField('Новый пароль',
                             validators = [DataRequired(), EqualTo('confirm', message='Пароли должны совпадать')])
    confirm = PasswordField('Повторите пароль', validators = [DataRequired()])
    submit = SubmitField("Регистрация")

class NewEntryForm(FlaskForm):
    text = TextAreaField("Текст", validators = [Length(max=250)])
    photos = MultipleFileField('Фото')
    submit = SubmitField("Добавить пост")

class EditProfileForms(FlaskForm):
    name = StringField('Имя пользователя', validators=[Length(min=4, max=25)])
    email = StringField("Email", validators=[Email()])
    about = TextAreaField("Текст", validators = [Length(max=100)])
    photo = FileField("Главное фото")
    submit = SubmitField("Изменить")

class ChangePasForm(FlaskForm):
    password = PasswordField('Старый пароль',
                             validators=[DataRequired()])
