from flask import Blueprint, render_template, abort, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import User, Lab, Submission
from ..forms import LabForm
from .. import db

bp = Blueprint('admin', __name__, url_prefix='/admin')

def _ensure_admin():
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        abort(403)

# ===== DASHBOARD (у тебя уже есть, оставь как есть) =====
@bp.route('/dashboard')
@login_required
def dashboard():
    _ensure_admin()
    users_count = User.query.count()
    labs_count = Lab.query.count()
    subs_count = Submission.query.count()

    last_subs = Submission.query.order_by(Submission.id.desc()).limit(5).all()

    # Топ-5 по числу верных решений (на небольших объёмах ок)
    stats = {}
    for s in Submission.query.all():
        st = stats.setdefault(s.user_id, {'ok': 0, 'total': 0})
        st['total'] += 1
        if s.is_correct:
            st['ok'] += 1
    top_users = []
    for uid, st in stats.items():
        u = User.query.get(uid)
        if u:
            top_users.append((u, st['ok'], st['total']))
    top_users.sort(key=lambda x: (-x[1], -x[2]))
    top_users = top_users[:5]

    return render_template('admin/dashboard.html',
                           users_count=users_count,
                           labs_count=labs_count,
                           subs_count=subs_count,
                           last_subs=last_subs,
                           top_users=top_users)

# ===== ЛАБЫ: список / создание / редактирование / удаление =====
@bp.route('/labs')
@login_required
def labs_list():
    _ensure_admin()
    labs = Lab.query.order_by(Lab.created_at.desc()).all()
    return render_template('admin/labs_list.html', labs=labs)

@bp.route('/labs/new', methods=['GET', 'POST'])
@login_required
def labs_new():
    _ensure_admin()
    form = LabForm()
    if form.validate_on_submit():
        lab = Lab(
            title=form.title.data.strip(),
            description=form.description.data.strip(),
            algorithm=form.algorithm.data.strip(),
            payload=form.payload.data.strip(),
            answer_hash=form.answer_hash.data.strip()
        )
        db.session.add(lab)
        db.session.commit()
        flash('Лаба создана', 'success')
        return redirect(url_for('admin.labs_list'))
    return render_template('admin/labs_form.html', form=form, lab=None)

@bp.route('/labs/<int:lab_id>/edit', methods=['GET','POST'])
@login_required
def labs_edit(lab_id):
    _ensure_admin()
    lab = Lab.query.get_or_404(lab_id)
    form = LabForm(obj=lab)
    if form.validate_on_submit():
        form.populate_obj(lab)
        db.session.commit()
        flash('Лаба обновлена', 'success')
        return redirect(url_for('admin.labs_list'))
    return render_template('admin/labs_form.html', form=form, lab=lab)

@bp.route('/labs/<int:lab_id>/delete', methods=['POST'])
@login_required
def labs_delete(lab_id):
    _ensure_admin()
    lab = Lab.query.get_or_404(lab_id)
    db.session.delete(lab)
    db.session.commit()
    flash('Лаба удалена', 'info')
    return redirect(url_for('admin.labs_list'))

# ===== ПОЛЬЗОВАТЕЛИ: список / карточка / (опц.) удаление =====
@bp.route('/users')
@login_required
def users_list():
    _ensure_admin()
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users_list.html', users=users)

@bp.route('/users/<int:user_id>')
@login_required
def user_detail(user_id):
    _ensure_admin()
    user = User.query.get_or_404(user_id)
    subs = (Submission.query
            .filter_by(user_id=user.id)
            .order_by(Submission.created_at.desc())
            .all())
    return render_template('admin/user_detail.html', user=user, subs=subs)

@bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def user_delete(user_id):
    _ensure_admin()
    if user_id == current_user.id:
        flash('Нельзя удалить самого себя', 'warning')
        return redirect(url_for('admin.users_list'))
    user = User.query.get_or_404(user_id)
    if getattr(user, 'is_admin', False):
        flash('Нельзя удалить администратора', 'warning')
        return redirect(url_for('admin.users_list'))
    # каскад для submissions — если не настроен на модели, удалим вручную
    Submission.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь удалён', 'info')
    return redirect(url_for('admin.users_list'))
