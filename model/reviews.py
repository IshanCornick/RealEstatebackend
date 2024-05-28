from datetime import datetime
from __init__ import db, app

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    def __init__(self, rating, comment):
        self.rating = rating
        self.comment = comment

    def read(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'comment': self.comment,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

def initReviews():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        r1 = Review(rating=5, comment='Great experience!')
        r2 = Review(rating=4, comment='Good service.')
        reviews = [r1, r2]
        for review in reviews:
            try:
                review.create()
            except Exception as e:
                print(f"Error creating review: {e}")
                db.session.rollback()
