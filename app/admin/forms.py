from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app.models import User

class AdminEditUserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=4, max=20)])
    first_name = StringField('名字', validators=[Length(max=50)])
    last_name = StringField('姓氏', validators=[Length(max=50)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[Length(min=6)])  # 移除DataRequired，允许不修改密码
    role = SelectField('角色', choices=[('user', '普通用户'), ('editor', '编辑'), ('admin', '管理员')], validators=[DataRequired()])
    submit = SubmitField('更新用户')

    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(AdminEditUserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        # 检查用户名是否被其他用户使用（排除当前用户）
        user = User.query.filter_by(username=username.data).first()
        if user and user.username != self.original_username:
            raise ValidationError('用户名已存在')

    def validate_email(self, email):
        # 检查邮箱是否被其他用户使用（排除当前用户）
        user = User.query.filter_by(email=email.data).first()
        if user and user.email != self.original_email:
            raise ValidationError('邮箱已被注册')