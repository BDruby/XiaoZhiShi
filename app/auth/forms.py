from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username_or_email = StringField('用户名或邮箱', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')
    
    def validate_username_or_email(self, field):
        # 移除Email验证器，因为我们现在接受用户名或邮箱
        pass

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=4, max=20)])
    first_name = StringField('名字', validators=[Length(max=50)])
    last_name = StringField('姓氏', validators=[Length(max=50)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('确认密码', validators=[
        DataRequired(),
        EqualTo('password', message='密码不匹配')
    ])
    submit = SubmitField('注册')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('用户名已存在')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('邮箱已被注册')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('当前密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[DataRequired(), Length(min=6)])
    new_password2 = PasswordField('确认新密码', validators=[
        DataRequired(),
        EqualTo('new_password', message='新密码不匹配')
    ])
    submit = SubmitField('修改密码')