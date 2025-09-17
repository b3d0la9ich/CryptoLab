from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from hashlib import sha256

from ..forms import CaesarForm, VigenereForm, AESForm, RSAForm
from ..crypto.caesar import caesar
from ..crypto.vigenere import vigenere
from ..crypto.aes import encrypt_cbc, decrypt_cbc
from ..crypto.rsa import encrypt_decrypt
from ..models import Lab, Submission
from ..forms import CaesarForm, VigenereForm, AESForm, RSAForm, RC4Form, PlayfairForm, RailFenceForm, SHA256Form
from ..crypto.rc4 import rc4_encrypt, rc4_decrypt
from ..crypto.playfair import playfair_encrypt, playfair_decrypt
from ..crypto.railfence import railfence_encrypt, railfence_decrypt
from ..crypto.sha256util import sha256_hex
import base64
from .. import db

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

# Песочницы
@bp.route('/playground/caesar', methods=['GET', 'POST'])
@login_required
def pg_caesar():
    form = CaesarForm()
    res = None
    if form.validate_on_submit():
        res = caesar(form.text.data, form.shift.data)
    return render_template('playground/caesar.html', form=form, result=res)

@bp.route('/playground/vigenere', methods=['GET', 'POST'])
@login_required
def pg_vigenere():
    form = VigenereForm()
    enc = dec = None
    if form.validate_on_submit():
        enc = vigenere(form.text.data, form.key.data, encrypt=True)
        dec = vigenere(enc, form.key.data, encrypt=False)
    return render_template('playground/vigenere.html', form=form, enc=enc, dec=dec)

@bp.route('/playground/aes', methods=['GET', 'POST'])
@login_required
def pg_aes():
    form = AESForm()
    enc = dec = None
    if form.validate_on_submit():
        key = form.key.data.encode('utf-8')
        enc = encrypt_cbc(form.text.data, key)
        dec = decrypt_cbc(enc, key)
    return render_template('playground/aes.html', form=form, enc=enc, dec=dec)

@bp.route('/playground/rsa', methods=['GET', 'POST'])
@login_required
def pg_rsa():
    form = RSAForm()
    enc = dec = None
    if form.validate_on_submit():
        enc, dec = encrypt_decrypt(form.text.data)
    return render_template('playground/rsa.html', form=form, enc=enc, dec=dec)

@bp.route('/playground/rc4', methods=['GET', 'POST'])
@login_required
def pg_rc4():
    form = RC4Form()
    enc_b64 = dec = None
    if form.validate_on_submit():
        ct = rc4_encrypt(form.text.data, form.key.data)
        enc_b64 = base64.b64encode(ct).decode('ascii')
        dec = rc4_decrypt(ct, form.key.data)
    return render_template('playground/rc4.html', form=form, enc=enc_b64, dec=dec)

@bp.route('/playground/playfair', methods=['GET', 'POST'])
@login_required
def pg_playfair():
    form = PlayfairForm()
    enc = dec = None
    if form.validate_on_submit():
        enc = playfair_encrypt(form.text.data, form.key.data)
        dec = playfair_decrypt(enc, form.key.data)
    return render_template('playground/playfair.html', form=form, enc=enc, dec=dec)

@bp.route('/playground/railfence', methods=['GET', 'POST'])
@login_required
def pg_railfence():
    form = RailFenceForm()
    enc = dec = None
    if form.validate_on_submit():
        enc = railfence_encrypt(form.text.data, form.rails.data)
        dec = railfence_decrypt(enc, form.rails.data)
    return render_template('playground/railfence.html', form=form, enc=enc, dec=dec)

@bp.route('/playground/sha256', methods=['GET', 'POST'])
@login_required
def pg_sha256():
    form = SHA256Form()
    digest = None
    if form.validate_on_submit():
        digest = sha256_hex(form.text.data)
    return render_template('playground/sha256.html', form=form, digest=digest)

# Лабы для студентов
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
        db.session.add(Submission(user_id=current_user.id, lab_id=lab.id,
                                  submitted_text=answer, is_correct=ok))
        db.session.commit()
    return render_template('playground/lab_solve.html', lab=lab, ok=ok, answer=answer)
