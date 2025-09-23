from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
from wtforms.validators import ValidationError


MAX_TEXT = 5000


# Мягкий email-валидатор: позволяет любые домены (в т.ч. .local),
# проверяет только базовый синтаксис user@domain
def any_domain_email(form, field):
    v = (field.data or "").strip()
    if "@" not in v or v.startswith("@") or v.endswith("@"):
        raise ValidationError("Неверный email")
    # можно добавить ещё чуть-чуть правил, но без проверки DNS/TLD

class ModeMixin:
    mode = RadioField(
        'Режим',
        choices=[('enc', 'Зашифровать'), ('dec', 'Расшифровать')],
        default='enc'
    )

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
class CaesarForm(FlaskForm, ModeMixin):
    text = TextAreaField('Текст', validators=[DataRequired(), Length(max=5000)])
    shift = IntegerField('Сдвиг', default=3, validators=[DataRequired(), NumberRange(min=-100, max=100)])
    submit = SubmitField('Выполнить')

class VigenereForm(FlaskForm, ModeMixin):
    text = TextAreaField('Текст', validators=[DataRequired(), Length(max=5000)])
    key = StringField('Ключ', validators=[DataRequired(), Length(min=1, max=64)])
    submit = SubmitField('Выполнить')

class PlayfairForm(FlaskForm, ModeMixin):
    text = TextAreaField('Текст', validators=[DataRequired(), Length(max=5000)])
    key = StringField('Ключевое слово', validators=[DataRequired(), Length(min=1, max=64)])
    submit = SubmitField('Выполнить')

class RC4Form(FlaskForm, ModeMixin):
    text = TextAreaField('Текст / Base64(шифртекст)', validators=[DataRequired(), Length(max=10000)])
    key = StringField('Ключ', validators=[DataRequired(), Length(min=1, max=256)])
    submit = SubmitField('Выполнить')

class RailFenceForm(FlaskForm, ModeMixin):
    text = TextAreaField('Текст', validators=[DataRequired(), Length(max=5000)])
    rails = IntegerField('Число рельс (2–10)', default=3, validators=[DataRequired(), NumberRange(min=2, max=10)])
    submit = SubmitField('Выполнить')

# AES — два поля для шифрования/дешифрования
class AESForm(FlaskForm):
    mode = RadioField('Режим', choices=[('enc', 'Зашифровать'), ('dec', 'Расшифровать')], default='enc')
    text = TextAreaField('Открытый текст', validators=[Optional(), Length(max=10000)])
    ctb64 = TextAreaField('Base64 (IV+CT)', validators=[Optional(), Length(max=20000)])
    key = StringField('Ключ (16/24/32 байта)', validators=[DataRequired(), Length(min=16, max=32)])
    submit = SubmitField('Выполнить (CBC)')

class RSAForm(FlaskForm):
    text = TextAreaField('Текст / Base64(шифртекст)', validators=[DataRequired()])

    submit = SubmitField('Выполнить')

    # Ограничение по байтам UTF-8 (≈ 190 для RSA-2048+OAEP(SHA-256))
    def validate_text(self, field):
        # Если мы шифруем — проверим лимит байтов. При расшифровке можно быть длиннее,
        # но здесь у нас режим только шифрования/демо, см. view ниже.
        if len(field.data.encode('utf-8')) > 190:
            raise ValidationError('Для RSA-2048 + OAEP(SHA-256) размер сообщения не должен превышать ~190 байт (в UTF-8 меньше 190 символов).')

class SHA256Form(FlaskForm):
    text = TextAreaField('Текст', validators=[DataRequired(), Length(max=10000)])
    submit = SubmitField('Посчитать хэш')


# Админ
class LabForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание', validators=[DataRequired()])
    algorithm = StringField('Алгоритм (caesar|vigenere|aes|rsa)', validators=[DataRequired()])
    payload = TextAreaField('Входные данные', validators=[DataRequired()])
    answer_hash = StringField('Ожидаемый ответ (SHA-256)', validators=[DataRequired(), Length(min=64, max=64)])
    submit = SubmitField('Сохранить')
