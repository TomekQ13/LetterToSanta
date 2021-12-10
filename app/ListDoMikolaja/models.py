from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from ListDoMikolaja import db, login_manager
from flask import current_app
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(128))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)    
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    letter = db.relationship('Letter', backref='author', lazy=True)
    friends_accepted = db.relationship('User', secondary='friends',
        primaryjoin = "Friends.accepted_id == User.id",
        secondaryjoin = "Friends.invited_id == User.id"
    )
    friends_invited = db.relationship('User', secondary='friends',
        primaryjoin = "Friends.invited_id == User.id",
        secondaryjoin = "Friends.accepted_id == User.id"
    )
    @property
    def friends(self):
        return self.friends_accepted + self.friends_invited

    requests_sent = db.relationship('FriendRequest',
        foreign_keys = 'FriendRequest.sent_by_id',
        backref = 'sender'
    )
    requests_received = db.relationship('FriendRequest',
        foreign_keys = 'FriendRequest.sent_to_id',
        backref = 'receiver'
    )
    letter_lines = db.relationship('LetterLine', backref='author', lazy=True)

    @property
    def taken_lines(self):
        results = LetterLine.query.filter(LetterLine.taken_user_id == self.id).all()
        return [{'line': result, 'taker': result.author} for result in results]

    @property
    def identifier(self):
        if self.name and self.surname:
            return self.name + ' ' + self.surname
        else:
            return self.username

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f"Role('{self.id}', '{self.name}')"

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"UserRoles('{self.id}', '{self.user_id}', '{self.role_id}')"

class Letter(db.Model):
    __tablename__ = 'letter'
    id = db.Column(db.Integer(), primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))

class Friends(db.Model):
    __tablename__ = 'friends'
    id = db.Column(db.Integer(), primary_key=True)
    invited_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    accepted_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    date_accepted = db.Column(db.DateTime, nullable=False, default = datetime.now)

    def __repr__(self):
        return f"Friends(date accepted: '{self.date_accepted}', invited: '{self.invited_id}', accepted: '{self.accepted_id}')"

class FriendRequest(db.Model):
    __tablename__ = 'friend_request'
    id = db.Column(db.Integer(), primary_key=True)
    sent_by_id =  db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    sent_to_id =  db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    date_sent = db.Column(db.DateTime, nullable=False, default = datetime.now)
    date_status_change = db.Column(db.DateTime)
    status_cd = db.Column(db.Integer(), nullable=False,
        default=0, comment="0-sent, 1-declined"
    )
    #status_cd 0-sent, 1-declined

    def __repr__(self):
        return f'FriendRequest(sent_by_id: {self.sent_by_id}, sent_to_id: {self.sent_to_id}, status_cd: {self.status_cd}'

class LetterLine(db.Model):
    __tablename__ = 'letter_line'
    line_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    line_content = db.Column(db.Text, nullable=False)
    taken = db.Column(db.Boolean, nullable=False, default=False)
    taken_user_id = db.Column(db.Integer())

    def __repr__(self):
        return f"LetterLine('{self.line_id}', '{self.user_id}', '{self.line_content}', '{self.taken}', '{self.taken_user_id}')"

    @property
    def line_taker(self):
        """
        Returns the taker of the letter line. None if doesn't exist.
        """
        query = User.query.filter(User.id == self.taken_user_id).first()
        return query

