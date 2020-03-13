from app import db,bcrypt

class Auctioner(db.Model):
    __tablename__ = 'auctioner'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    phone  = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(), nullable=False)

    # CREATE
    def insert_record(self):
        db.session.add(self)
        db.session.commit()

    # check if a auctioner exist
    @classmethod
    def check_email_exist(cls,email):
        record = cls.query.filter_by(email=email).first()
        if record:
            return True
        else:
            return False

    # validate password
    @classmethod
    def validate_password(cls,email,password):
        record = cls.query.filter_by(email=email).first()
        if record and bcrypt.check_password_hash(record.password,password):
            return True
        else:
            return False

    # get auctioner id
    @classmethod
    def get_auctioner_id(cls,email):
        return cls.query.filter_by(email=email).first().id