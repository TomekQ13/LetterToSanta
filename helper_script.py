from ListDoMikolaja import db, create_app

app = create_app()
app.app_context().push()

from ListDoMikolaja.models import FriendRequest, LetterLine, User
from ListDoMikolaja.models import Friends

db.drop_all()
db.create_all()



user1 = User(username='tkuczak',email='asd',password='aaa', name='Tomasz', surname='KKKKK')
db.session.add(user1)
db.session.commit()

user2 = User(username='tkuczak2',email='asddddd',password='aaa')
db.session.add(user2)
db.session.commit()

friend = Friends(id = 1,invited_id = 1,accepted_id = 2)
db.session.add(friend)
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
request2 = FriendRequest(sent_to_id=2, sent_by_id=1, status_cd=0)
db.session.add(request1)
db.session.commit()
db.session.add(request2)
db.session.commit()
db.session.add(request3)
db.session.commit()

letter_line1=LetterLine(user_id=1, line_content='asdasdavsdv')
db.session.add(letter_line1)
letter_line2=LetterLine(
    user_id=1,
    line_content='sssdsdsddsdsds',
    taken=1,
    taken_user_id=1
)
db.session.add(letter_line2)
db.session.commit()

lt = LetterLine.query.get(2)