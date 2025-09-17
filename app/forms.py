from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange


# Мягкий email-валидатор: позволяет любые домены (в т.ч. .local),
# проверяет только базовый синтаксис user@domain
def any_domain_email(form, field):
    v = (field.data or "").strip()
    if "@" not in v or v.startswith("@") or v.endswith("@"):
        raise ValidationError("Неверный email")
    # можно добавить ещё чуть-чуть правил, но без проверки DNS/TLD

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), any_domain_email])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), any_domain_email])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Повтор пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

# Песочницы
class CaesarForm(FlaskForm):
    text = TextAreaField('Текст', validators=[DataRequired()])
    shift = IntegerField('Сдвиг', default=3, validators=[DataRequired(), NumberRange(min=-100, max=100)])
    submit = SubmitField('Выполнить')

class VigenereForm(FlaskForm):
    text = TextAreaField('Текст', validators=[DataRequired()])
    key = StringField('Ключ', validators=[DataRequired(), Length(min=1, max=64)])
    submit = SubmitField('Выполнить')

class AESForm(FlaskForm):
    text = TextAreaField('Текст', validators=[DataRequired()])
    key = StringField('Ключ (16/24/32 байта)', validators=[DataRequired(), Length(min=16, max=32)])
    submit = SubmitField('Зашифровать (CBC)')

class RSAForm(FlaskForm):
    text = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Зашифровать/Расшифровать с новым ключом')

class RC4Form(FlaskForm):
    text = TextAreaField('Текст', validators=[DataRequired()])
    key = StringField('Ключ', validators=[DataRequired(), Length(min=1, max=256)])
    submit = SubmitField('Выполнить')

class PlayfairForm(FlaskForm):
    text = TextAreaField('Текст', validators=[DataRequired()])
    key = StringField('Ключевое слово', validators=[DataRequired(), Length(min=1, max=32)])
    submit = SubmitField('Выполнить')

class RailFenceForm(FlaskForm):
    text = TextAreaField('Текст', validators=[DataRequired()])
    rails = IntegerField('Число рельс (2–10)', default=3,
                         validators=[DataRequired(), NumberRange(min=2, max=10)])
    submit = SubmitField('Выполнить')

class SHA256Form(FlaskForm):
    text = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Посчитать хэш')


# Админ
class LabForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание', validators=[DataRequired()])
    algorithm = StringField('Алгоритм (caesar|vigenere|aes|rsa)', validators=[DataRequired()])
    payload = TextAreaField('Входные данные', validators=[DataRequired()])
    answer_hash = StringField('Ожидаемый ответ (SHA-256)', validators=[DataRequired(), Length(min=64, max=64)])
    submit = SubmitField('Сохранить')
