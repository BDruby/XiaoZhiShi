from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    """装饰器：确保用户具有管理员权限"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['admin', 'editor']:
            abort(403)  # 禁止访问
        return f(*args, **kwargs)
    return decorated_function