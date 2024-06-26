from utils.conn import db

class TopKeywords(db.Model):
    __tablename__ = 'top_keywords'

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(50))
    channel_name = db.Column(db.String(50))
    top_keywords = db.Column(db.Text(collation='utf8mb4_unicode_ci'))
    

    def __repr__(self):
        return f'<TopKeywords {self.channel_id}>'
