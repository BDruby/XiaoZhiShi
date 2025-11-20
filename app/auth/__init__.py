from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, Setting
from app.auth.forms import LoginForm, RegisterForm, ChangePasswordForm

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # 检查是邮箱还是用户名
        username_or_email = form.username_or_email.data
        if '@' in username_or_email:
            # 这是一个邮箱地址
            user = User.query.filter_by(email=username_or_email).first()
        else:
            # 这是一个用户名
            user = User.query.filter_by(username=username_or_email).first()
        
        if user and user.check_password(form.password.data):
            # 检查用户是否被禁用
            if not user.is_active:
                flash('您的账户已被禁用，请联系管理员', 'error')
                return render_template('auth/login.html', form=form)
                
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        flash('无效的用户名/邮箱或密码', 'error')
    
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # 检查注册是否开放
    registration_open_setting = Setting.query.filter_by(key='registration_open').first()
    if registration_open_setting and registration_open_setting.value == 'false':
        flash('当前暂不开放注册', 'error')
        return redirect(url_for('auth.login'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！请登录。', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('当前密码错误', 'error')
            return render_template('auth/change_password.html', form=form)
        
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('密码修改成功', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('auth/change_password.html', form=form)