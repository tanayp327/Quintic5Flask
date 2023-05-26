from __init__ import db
from sqlalchemy.exc import IntegrityError
import json

class LeaderboardEntry(db.Model):
    __tablename__ = 'leaderboard'

    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, rank, name, score):
        self.rank = rank
        self.name = name
        self.score = score

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        return {
            "id": self.id,
            "rank": self.rank,
            "name": self.name,
            "score": self.score
        }

    def update(self, rank=None, name=None, score=None):
        if rank is not None:
            self.rank = rank
        if name is not None:
            self.name = name
        if score is not None:
            self.score = score

        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    def __str__(self):
        return json.dumps(self.read())

    def __repr__(self):
        return f'LeaderboardEntry(id={self.id}, rank={self.rank}, name={self.name}, score={self.score})'

def initLeaderboard():
    db.create_all()

# Uncomment the following line if you want to create some initial data
# initLeaderboard()
