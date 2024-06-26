from utils.conn import db

class Trends(db.Model):
    __tablename__ = 'trends'

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(50))
    channel_name = db.Column(db.String(50))
    views = db.Column(db.Integer)
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    

    def __repr__(self):
        return f'<Trends {self.channel_id}>'
