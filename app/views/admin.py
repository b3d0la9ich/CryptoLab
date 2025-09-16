from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..forms import LabForm
from ..models import Lab, Submission
from .. import db

bp = Blueprint('admin', __name__)

def admin_required():
    return current_user.is_authenticated and current_user.is_admin

@bp.before_request
def protect():
    # Блокируем любые admin-роуты для не-админов
    if request.blueprint == 'admin' and not admin_required():
        return redirect(url_for('auth.login'))

@bp.route('/labs', methods=['GET', 'POST'])
@login_required
def labs():
    form = LabForm()
    if form.validate_on_submit():
        lab = Lab(
            title=form.title.data,
            description=form.description.data,
            algorithm=form.algorithm.data.lower(),
            payload=form.payload.data,
            answer_hash=form.answer_hash.data.lower()
        )
        db.session.add(lab)
        db.session.commit()
        flash('Лаба сохранена', 'success')
        return redirect(url_for('admin.labs'))
    labs = Lab.query.order_by(Lab.id.desc()).all()
    return render_template('admin/labs.html', form=form, labs=labs)

@bp.route('/submissions')
@login_required
def submissions():
    subs = Submission.query.order_by(Submission.id.desc()).all()
    return render_template('admin/submissions.html', subs=subs)
