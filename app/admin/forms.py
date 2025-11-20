from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from app.models import User

class AdminEditUserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=4, max=20)])
    first_name = StringField('名字', validators=[Length(max=50)])
    last_name = StringField('姓氏', validators=[Length(max=50)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[Optional(), Length(min=6)])
    role = SelectField('角色', choices=[('user', '普通用户'), ('editor', '编辑'), ('admin', '管理员')], validators=[DataRequired()])
    is_active = BooleanField('账户状态 (启用/禁用)')
    bio = TextAreaField('个人简介', validators=[Length(max=500)])
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

class NavigationForm(FlaskForm):
    name = StringField('导航名称', validators=[DataRequired(), Length(max=100)])
    title = StringField('显示标题', validators=[DataRequired(), Length(max=100)])
    url = StringField('URL地址', validators=[DataRequired(), Length(max=500)])
    target = SelectField('打开方式', choices=[('_self', '当前窗口'), ('_blank', '新窗口')], default='_self')
    position = StringField('排序位置', validators=[DataRequired()], default=0)
    is_active = BooleanField('是否激活', default=True)
    submit = SubmitField('保存导航')