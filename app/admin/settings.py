from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.admin import bp
from app.models import db, Setting

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if current_user.role != 'admin':
        flash('只有管理员可以访问设置页面', 'error')
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        # 处理注册开关
        registration_open = request.form.get('registration_open') == 'on'
        
        # 保存设置
        setting = Setting.query.filter_by(key='registration_open').first()
        if not setting:
            setting = Setting(key='registration_open', type='boolean')
            db.session.add(setting)
            
        setting.value = 'true' if registration_open else 'false'
        
        db.session.commit()
        flash('设置已更新', 'success')
        return redirect(url_for('admin.settings'))
    
    # 获取当前设置
    registration_open_setting = Setting.query.filter_by(key='registration_open').first()
    registration_open = registration_open_setting.value == 'true' if registration_open_setting else True
    
    return render_template('admin/settings.html', registration_open=registration_open)
