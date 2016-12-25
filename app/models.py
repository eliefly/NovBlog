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
        u4 = User(username='editor1', email='editor1@example.com', role='editor')
        u5 = User(username='editor2', email='editor2@example.com', role='editor')
        u1.password = 'novblog1'
        u2.password = 'novblog2'
        u3.password = 'admin'
        u4.password = 'editor1'
        u5.password = 'editor2'
        u1.save()
        u2.save()
        u3.save()
        u4.save()
        u5.save()


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

class Comment(db.EmbeddedDocument):
    content = db.StringField()
    name = db.StringField(max_length=120)

post_status = (('草稿', '草稿'), ('发布', '发布'))

class Post(db.Document):
    title = db.StringField(max_length=120, required=True)
    # CASCADE (2) - Deletes the documents associated with the reference.
    author = db.ReferenceField(User, reverse_delete_rule=2)
    category = db.StringField(max_length=64)    
    tags = db.ListField(db.StringField(max_length=30))
    content = db.StringField()
    status = db.StringField(required=True, choices=post_status)
    publish_time = db.DateTimeField(default=datetime.now)
    modifly_time = db.DateTimeField(default=datetime.now)
    comments = db.ListField(db.EmbeddedDocumentField(Comment))

    # 想法：Post和图片可视作一对多关系，Image可直接在Post中放一个类似comments的字段
    # Images = db.ListField(db.EmbeddedDocumentField(PostImage))

    meta = {'allow_inheritance': True,
            'ordering': ['-publish_time']}

    @staticmethod
    def generate_fake(count=30):
        '''生成虚拟博客文章'''
        from random import seed, randint
        import forgery_py

        seed()
        editor_user = User.objects(role='editor')
        user_count = editor_user.count()
        for i in range(count):
            u = editor_user[randint(0, user_count-1)]
            post = Post(title='blog title ' + str(i), author=u)
            post.content = forgery_py.lorem_ipsum.sentences(randint(1, 50))
            post.category = ['web', 'linux', 'python'][randint(0,2)]
            post.tags = ['html', 'css', 'mongodb', 'mysql', 'javascript', 'flask'][randint(0, 5):randint(0, 5)]
            post.status = ['草稿', '发布'][randint(0, 1)]
            post.save()


# 先实现简单的博客内容，content直接放在Post类中。后续在考虑其他内容。
# class TextPost(Post):
#     content = db.StringField()
#
#
#     @staticmethod
#     def insert_textpost():
#         post1 = TextPost(title='Fun with MongoEngine', author='john')
#         post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
#         post1.tags = ['mongodb', 'mongoengine']
#         post1.save()
#
# class ImagePost(Post):
#     image_path = db.StringField()
#
# class LinkPost(Post):
#     link_url = db.StringField()
#
#     @staticmethod
#     def insert_linkpost():
#         post2 = LinkPost(title='MongoEngine Documentation', author='ross')
#         post2.link_url = 'http://docs.mongoengine.com/'
#         post2.tags = ['mongoengine']
#         post2.save()
