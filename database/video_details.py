from utils.conn import db

class VideoDetails(db.Model):
    __tablename__ = 'video_details'

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(50), nullable=False)
    title = db.Column(db.Text(collation='utf8mb4_unicode_ci'), nullable=False)
    description = db.Column(db.Text(collation='utf8mb4_unicode_ci'))
    view_count = db.Column(db.Integer)
    like_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    publication_date = db.Column(db.String(50))
    channel_id = db.Column(db.String(50))
    channel_name=db.Column(db.Text(collation='utf8mb4_unicode_ci'))

    def __repr__(self):
        return f'<VideoDetails {self.title}>'
