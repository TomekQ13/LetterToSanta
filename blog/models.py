from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from blog import db, login_manager
from flask import current_app
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=0)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comments', backref='author', lazy=True)
    roles = db.relationship('Role', secondary='user_roles',  backref=db.backref('user', lazy=True), lazy='subquery')

    @property
    def roles_names(self):
        return [role.name for role in User.query.get(self.id).roles]

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(128),nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.now)
    comments = db.relationship('Comments', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f"Role('{self.id}', '{self.name}')"

class UserRoles(db.Model):
    __tablename__='user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"UserRoles('{self.id}', '{self.user_id}', '{self.role_id}')"

class Comments(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.now)

    def __repr__(self):
        return f"Comments('{self.id}', '{self.post_id}', '{self.author_id}')"

