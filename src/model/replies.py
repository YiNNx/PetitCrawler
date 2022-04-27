from videos import db

class Replies(db.Model):

    __tablename__ = "replies"
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
    content = db.Column(db.String(512))

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    
    def query(aid):
        video = Replies.query.filter(Replies.oid==aid).first()
        return video

if __name__ == '__main__':
        reply=Replies(
            rpid=1
        )
        reply.insert()
