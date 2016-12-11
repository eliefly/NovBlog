from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, \
                RadioField, SelectField, FileField
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


class EditUserProfileForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(1, 64),
                            Regexp('^[A-Za-z_][A-Za-z0-9_.]*$', 0, '用户名必须是字母数字和下划线组成')])
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email()])
    about_me = StringField('介绍', validators=[Length(0, 256)])
    submit = SubmitField('保存')

    def __init__(self, user, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.objects.filter(email=field.data).count() > 0:
            raise ValidationError('邮箱已经被使用！')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.objects.filter(username=field.data).count() > 0:
            raise ValidationError('用户名已经被使用！')


class AvatarForm(FlaskForm):
    avatar = FileField('头像')
    submit = SubmitField('上传')