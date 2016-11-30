from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, \
                RadioField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User, ROLES

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[Required()])
    password = PasswordField('密码', validators=[Required(), Length(1, 10)])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[Required(), Length(1, 64),
                            Regexp('^[A-Za-z_][A-Za-z0-9_.]*$', 0, '用户名必须是字母数字和下划线组成')])
    password = PasswordField('密码', validators=[Required(), EqualTo('password2', message='两次密码必须一致')])
    password2 = PasswordField('确认密码', validators=[Required()])
    role = SelectField('角色权限', choices=ROLES)
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.objects.filter(email=field.data).count() > 0:
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if User.objects.filter(username=field.data).count() > 0:
            raise ValidationError('用户名已被使用')
