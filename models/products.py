from app import db

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(), nullable=False)
    pname = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    initbid = db.Column(db.String(), nullable=False)
    # 0-sold 1-ongoing
    status = db.Column(db.String(), nullable=False, default='1')
    

    # insert record
    def insert_record(self):
        db.session.add(self)
        db.session.commit()
    
    # fetch all Products
    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    # fetch where status is 1
    @classmethod
    def fetch_by_status_onsale(cls):
        return cls.query.filter_by(status=u'1')

    # update status
        # update a product
    @classmethod
    def update_product_by_id(cls,id,status=None):
        product = cls.query.filter_by(id=id).first()

        if product:
            if status:
                product.status = status
            db.session.commit()
            return True    
        else:
            return False

    # delete product by id
    @classmethod
    def delete_by_id(cls,id):
        product = cls.query.filter_by(id=id)
        if product.first():
            product.delete()
            db.session.commit()
            return True
        else:
            return False

        