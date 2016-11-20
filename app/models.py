from werkzeug.security import generate_password_hash, check_password_hash
from . import db

ROLES = (('admin', 'admin'),
		('editor', 'editor'),
		('reader', 'reader'))

class User(db.Document):
	username = db.StringField(max_length=64, required=True)
	eamil = db.StringField(max_length=64, required=True)
	password_hash = db.StringField(required=True)
	role = db.StringField(max_length=32, default='reader', choices=ROLES)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
		

