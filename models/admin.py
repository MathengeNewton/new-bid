from app import db

class AdminModel(db.Model):
    __tablename__ = 'adminstrators'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False,unique=True)
    phone_number = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    # insert record
    def insert_record(self):
        db.session.add(self)
        db.session.commit()