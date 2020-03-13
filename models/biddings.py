from app import db

class Biddings(db.Model):
    __tablename__ = 'bidding'
    id = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    bid_amount = db.Column(db.String(50), nullable=False)

    # create
    def insert_record(self):
        db.session.add(self)
        db.session.commit()

    # fetch all
    @classmethod
    def fetch_all(cls):
        return cls.query.all()