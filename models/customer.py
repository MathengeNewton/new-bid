from app import db,bcrypt

class CustomerModel(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False,unique=True)
    phone_number = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    

    # insert record
    def insert_record(self):
        db.session.add(self)
        db.session.commit()
    
    # check if email is in use
    @classmethod
    def check_email_exist(cls,email):
        customer = cls.query.filter_by(email=email).first()
        if customer:
            return True
        else:
            return False

    # validate password
    @classmethod
    def validate_password(cls,email,password):
        customer = cls.query.filter_by(email=email).first()

        if customer and bcrypt.check_password_hash(customer.password,password):
            return True
        else:
            return False

    # get customer id
    @classmethod
    def get_customer_id(cls,email):
        return cls.query.filter_by(email=email).first().id


