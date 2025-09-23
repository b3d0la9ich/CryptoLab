# app/views/main.py
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from hashlib import sha256

from .. import db
from ..models import Lab, Submission

# Формы
from ..forms import (
    CaesarForm, VigenereForm, AESForm, RSAForm,
    RC4Form, PlayfairForm, RailFenceForm, SHA256Form
)

# Крипто-утилиты
from ..crypto.caesar import caesar_encrypt, caesar_decrypt
from ..crypto.vigenere import vigenere
from ..crypto.aes import encrypt_cbc, decrypt_cbc
from ..crypto.rsa import generate_keypair_pem, rsa_encrypt_b64, rsa_decrypt_b64
from ..crypto.rc4 import rc4_encrypt_b64, rc4_decrypt_b64
from ..crypto.playfair import playfair_encrypt, playfair_decrypt
from ..crypto.railfence import railfence_encrypt, railfence_decrypt

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/profile')
@login_required
def profile():
    subs = (Submission.query
            .filter_by(user_id=current_user.id)
            .order_by(Submission.id.desc())
            .all())
    return render_template('profile.html', subs=subs)

# ===== Песочницы =====

@bp.route('/playground/caesar', methods=['GET', 'POST'])
@login_required
def pg_caesar():
    form = CaesarForm()
    result = None
    if form.validate_on_submit():
        txt = form.text.data
        shift = form.shift.data
        if getattr(form, 'mode', None) and form.mode.data == 'enc':
            result = caesar_encrypt(txt, shift)
        else:
            # по умолчанию — расшифровка, если mode нет
            result = caesar_decrypt(txt, shift)
    return render_template('playground/caesar.html', form=form, result=result)

@bp.route('/playground/vigenere', methods=['GET', 'POST'])
@login_required
def pg_vigenere():
    form = VigenereForm()
    result = None
    if form.validate_on_submit():
        txt = form.text.data
        key = form.key.data
        if form.mode.data == 'enc':
            result = vigenere(txt, key, encrypt=True)
        else:
            result = vigenere(txt, key, encrypt=False)
    return render_template('playground/vigenere.html', form=form, result=result)

@bp.route('/playground/aes', methods=['GET', 'POST'])
@login_required
def pg_aes():
    form = AESForm()
    enc = dec = err = None
    if form.validate_on_submit():
        try:
            key = form.key.data.encode('utf-8')
            if getattr(form, 'mode', None) and form.mode.data == 'enc':
                enc = encrypt_cbc(form.text.data, key)
                dec = decrypt_cbc(enc, key)  # проверка
            else:
                # расшифровка из Base64 (IV||CT)
                ctb64 = getattr(form, 'ctb64', None)
                if ctb64 is None or not ctb64.data:
                    raise ValueError('Не указан шифртекст Base64.')
                dec = decrypt_cbc(ctb64.data, key)
                enc = ctb64.data
        except Exception as e:
            err = f'Ошибка AES: {e}'
    return render_template('playground/aes.html', form=form, enc=enc, dec=dec, err=err)

@bp.route('/playground/rsa', methods=['GET', 'POST'])
@login_required
def pg_rsa():
    form = RSAForm()
    enc = dec = pub_pem = priv_pem = None
    if form.validate_on_submit():
        text = (form.text.data or '').strip()
        try:
            priv_pem, pub_pem = generate_keypair_pem(bits=2048)
            enc = rsa_encrypt_b64(text, pub_pem)
            dec = rsa_decrypt_b64(enc, priv_pem)
        except Exception as e:
            flash(f'Ошибка RSA: {e}', 'danger')
    return render_template('playground/rsa.html',
                           form=form, enc=enc, dec=dec,
                           pub_pem=pub_pem, priv_pem=priv_pem)

@bp.route('/playground/rc4', methods=['GET', 'POST'])
@login_required
def pg_rc4():
    form = RC4Form()
    enc = dec = err = None
    if form.validate_on_submit():
        try:
            txt = form.text.data
            key = form.key.data
            if getattr(form, 'mode', None) and form.mode.data == 'enc':
                enc = rc4_encrypt_b64(txt, key)
                dec = rc4_decrypt_b64(enc, key)  # проверка
            else:
                # расшифровка из Base64
                dec = rc4_decrypt_b64(txt, key)
                enc = txt
        except Exception as e:
            err = f'Ошибка RC4: {e}'
    return render_template('playground/rc4.html', form=form, enc=enc, dec=dec, err=err)

@bp.route('/playground/playfair', methods=['GET', 'POST'])
@login_required
def pg_playfair():
    form = PlayfairForm()
    enc = dec = err = None
    if form.validate_on_submit():
        try:
            txt = form.text.data
            key = form.key.data
            if getattr(form, 'mode', None) and form.mode.data == 'enc':
                enc = playfair_encrypt(txt, key)
                dec = playfair_decrypt(enc, key)  # проверка
            else:
                dec = playfair_decrypt(txt, key)
                enc = txt
        except Exception as e:
            err = f'Ошибка Playfair: {e}'
    return render_template('playground/playfair.html', form=form, enc=enc, dec=dec, err=err)

@bp.route('/playground/railfence', methods=['GET', 'POST'])
@login_required
def pg_railfence():
    form = RailFenceForm()
    result = None
    if form.validate_on_submit():
        txt = form.text.data
        rails = form.rails.data
        if getattr(form, 'mode', None) and form.mode.data == 'enc':
            result = railfence_encrypt(txt, rails)
        else:
            result = railfence_decrypt(txt, rails)
    return render_template('playground/railfence.html', form=form, result=result)

@bp.route('/playground/sha256', methods=['GET', 'POST'])
@login_required
def pg_sha256():
    form = SHA256Form()
    digest = None
    if form.validate_on_submit():
        import hashlib
        digest = hashlib.sha256(form.text.data.encode('utf-8')).hexdigest()
    return render_template('playground/sha256.html', form=form, digest=digest)

# ===== Лабы =====

@bp.route('/labs')
@login_required
def labs_list():
    labs = Lab.query.order_by(Lab.id.desc()).all()
    return render_template('playground/labs_list.html', labs=labs)

@bp.route('/labs/<int:lab_id>', methods=['GET', 'POST'])
@login_required
def solve_lab(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    answer = None
    ok = None
    if 'answer' in request.form:
        answer = request.form['answer']
        ok = (sha256(answer.encode()).hexdigest().lower() == lab.answer_hash.lower())
        db.session.add(Submission(user_id=current_user.id,
                                  lab_id=lab.id,
                                  submitted_text=answer,
                                  is_correct=ok))
        db.session.commit()
    return render_template('playground/lab_solve.html', lab=lab, ok=ok, answer=answer)
