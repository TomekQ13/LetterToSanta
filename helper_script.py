from ListDoMikolaja import db, create_app

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

from ListDoMikolaja.models import FriendRequest, User
from ListDoMikolaja.models import Friends

user1 = User(username='tkuczak',email='asd',password='aaa')
db.session.add(user1)
db.session.commit()

user2 = User(username='tkuczak2',email='asddddd',password='aaa')
db.session.add(user2)
db.session.commit()

friend = Friends(id = 1,invited_id = 1,accepted_id = 2)
db.session.add(friend)
db.session.commit()

friend2 = Friends(invited_id = 2,accepted_id = 1)
db.session.add(friend2)
db.session.commit()

tk = User.query.get(1)
tk2 = User.query.get(2)

user3 = User(username='tkuczak3',email='asssssddddd',password='aaa')
db.session.add(user3)
db.session.commit()

friend3 = Friends(invited_id = 1,accepted_id = 3)
db.session.add(friend3)
db.session.commit()

request1 = FriendRequest(sent_to_id=1, sent_by_id=3)
request3 = FriendRequest(sent_to_id=1, sent_by_id=2, status_cd=1)
request2 = FriendRequest(sent_to_id=2, sent_by_id=1)
db.session.add(request1)
db.session.commit()
db.session.add(request2)
db.session.commit()
db.session.add(request3)
db.session.commit()
