from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime

ROLES = (('admin', 'admin'),
        ('editor', 'editor'),
        ('reader', 'reader'))

class User(db.Document):
    username = db.StringField(max_length=64, required=True)
    email = db.StringField(max_length=64, required=True)
    password_hash = db.StringField(required=True)
    role = db.StringField(max_length=32, default='reader', choices=ROLES)
    about_me = db.StringField(max_length=256, default='这家伙很懒什么都没留下...')
    avatar = db.ImageField(size=(128, 128, True))
    # avatar = db.FileField()  # 0.8版本falsk-mongoengine bug不能上传图像出错，参见Document and fix connection code #280
    is_superuser = db.BooleanField(default=False)
    create_time = db.DateTimeField(default=datetime.now)
    last_login = db.DateTimeField(default=datetime.now)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # flask-login要求实现的的用户方法。因为UserMixin包含这些方法的默认实现，省去显式实现。
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return self.username
        except AttributeError:
            raise NotImplementedError('No `username` attribute - override `get_id`')

    def ping(self):
        '''更新用户最后的访问时间'''
        self.last_login = datetime.now()
        self.save()

    @staticmethod
    def insert_test_user():
        u1 = User(username='novblog1', email='novblog1@example.com')
        u2 = User(username='novblog2', email='novblog2@example.com')
        u3 = User(username='admin', email='admin@example.ocm', role='admin')
        u1.password = 'novblog1'
        u2.password = 'novblog2'
        u3.password = 'admin'
        u1.save()
        u2.save()
        u3.save()


    def __str__(self):
        return 'User %r' % self.username
        

# flask-login回调函数。如果找到用户返回用会对象，否则应返回None
@login_manager.user_loader
def load_user(username):
    # return User.objects.get(username=username)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user





# class ContentResource(Resource):
#     document = Content
  
# class Post(db.Document):
#     title = db.StringField(max_length=120, required=True)
#     description = db.StringField(max_length=120, required=False)
#     author = db.ReferenceField(User)
#     editor = db.ReferenceField(User)
#     tags = db.ListField(db.StringField(max_length=30))
#     user_lists = db.ListField(db.SafeReferenceField(User))
#     sections = db.ListField(db.EmbeddedDocumentField(Content))
#     content = db.EmbeddedDocumentField(Content)
#     is_published = db.BooleanField()