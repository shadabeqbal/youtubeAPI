from utils.conn import db

class AnalyzeMetrics(db.Model):
    __tablename__ = 'analyze_metrics'

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(50))
    channel_name = db.Column(db.String(50))
    total_like = db.Column(db.Integer)
    total_comments = db.Column(db.Integer)
    average_likes = db.Column(db.Float)
    average_comments = db.Column(db.Float)
    engagement_rate = db.Column(db.Float)

    def __repr__(self):
        return f'<AnalyzeMetrics {self.channel_id}>'
