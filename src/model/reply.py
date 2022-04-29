from model.video import db

class Replies(db.Model):

    __tablename__ = "replies"
    __table_args__ = {'mysql_charset' : 'utf8mb4'}
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    rpid = db.Column(db.Integer)
    oid = db.Column(db.Integer)
    mid = db.Column(db.Integer)
    root = db.Column(db.Integer)
    dialog = db.Column(db.Integer)
    rcount = db.Column(db.Integer)
    ctime = db.Column(db.Integer)
    like= db.Column(db.Integer)
    uname = db.Column(db.String(128))
    content = db.Column(db.String(1024))

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
    
    def query(aid):
        reply = Replies.query.filter(Replies.oid==aid).first()
        return reply


def addReply(data):
    reply=Replies(
        rpid = data['rpid'],
        oid = data['oid'],
        mid = data['mid'],
        root = data['root'],
        dialog = data['dialog'],
        rcount = data['rcount'],
        ctime = data['ctime'],
        like = data['like'],
        uname = data['member']['uname'],
        content = data['content']['message'],
    )
    print("user: "+data['member']['uname'])
    print("likes: "+str(data['like']))
    print("content: "+data['content']['message'])
    reply.insert()

