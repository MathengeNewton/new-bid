from flask import  Flask,render_template,redirect,url_for,flash,request,session
from flask_sqlalchemy import SQLAlchemy
# from werkzeug import secure_filename
from PIL import Image
from flask_bcrypt import Bcrypt
import time


import os

from config.config import *

# the upload folder for the images
UPLOAD_FOLDER = os.getcwd() + '/static/images/uploads'
# limit the number of extensions allowed
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# flask instance
app = Flask(__name__)
# config file
app.config.from_object(DevelopmentConfig)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# sqlalchemy instance
db = SQLAlchemy(app)
# flask bcrypt instance
bcrypt = Bcrypt(app)

from models.admin import AdminModel
from models.auctioner import Auctioner
from models.biddings import Biddings
from models.customer import CustomerModel
from models.products import Products


@app.before_first_request
def create_tables():
    db.create_all()

# create a function that check if an extension is valid, uploads a file and redirect user to url for image
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# create a function that uploads files
def upload_file(imageFile):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in imageFile:
            print('No file part')
            return None

        file = imageFile['file']

        # if user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            return None
        if file and allowed_file(file.filename):
            img = Image.open(file)
            new_width = 150
            new_height = 150
            size = (new_height,new_width)
            img = img.resize(size)
            stamped = int(time.time())
            print('all good')
            img.save(os.path.join(UPLOAD_FOLDER,str(stamped) + file.filename))
            print(os.path.join(UPLOAD_FOLDER,str(stamped) + file.filename))
            return '/static/images/uploads/'+ str(stamped) + file.filename
        else:
            return None

# landing page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auctioner/register', methods=['GET','POST'])
def auctioner_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirmpass = request.form['confirmpass']

        if password != confirmpass:
            flash('Passwords dont match','danger')
            return redirect(url_for('auctioner_register'))
        elif(Auctioner.check_email_exist(email)):
            flash('Email already in use','danger')
            return redirect(url_for('auctioner_register'))
        else:
            hashpassword = bcrypt.generate_password_hash(password).decode('utf-8')

            y = Auctioner(name=name,email=email,phone=phone,password=hashpassword)
            y.insert_record()

            flash('Account successfully created','success')
            return redirect(url_for('auctioner_login'))

    return render_template('auctionerregister.html')

    

# auctioner login
@app.route('/auctioner/login', methods=['GET','POST'])
def auctioner_login():
    if request.method == 'POST':
        # try:
        email = request.form['email']
        password = request.form['password']

        # check if email exist
        if Auctioner.check_email_exist(email):
            if Auctioner.validate_password(email=email,password=password):
                session['email'] = email
                session['uid'] = Auctioner.get_auctioner_id(email)
                return redirect(url_for('auctioner'))
            else:
                flash('Invalid login credentials','danger')
                return redirect(url_for('auctioner_login'))
        else:
            flash('Invalid login credentials', 'danger')
            return redirect(url_for('auctioner_login'))
    # except Exception as e:
        # print(e)
    
    return render_template('auctionerlogin.html')
    


#autioner registration
@app.route('/home', methods=['GET','POST'])
def auctioner():
    if session:
        if request.method == 'POST':
            print(session['email'])
            image_url = upload_file(request.files)
            pname = request.form['pname']
            description = request.form['description']
            bid = request.form['bid']
            
            x = Products(img=image_url,pname=pname,description=description,initbid=bid)
            x.insert_record()

            print('record successfully added')

            return redirect(url_for('auctioner'))
    else:
        return redirect(url_for('auctioner_login'))


    return render_template('auctioner.html')


@app.route('/bidding', methods=['GET','POST'])
def bid():
    if session:
        if request.method == 'POST':
            productname = request.form['productname']
            email = session['email']
            bid_price = request.form['bid_amount']

            b = Biddings(productname=productname,email=email,bid_amount=bid_price)
            b.insert_record()
            print('bidding successfull accepted')

            return redirect(url_for('home'))
    else:
        return redirect(url_for('auctioner_login'))

# view products
@app.route('/products/all', methods=['GET','POST'])
def products_all():
    allp = Products.fetch_all()

    return render_template('allproducts.html', allp=allp)

# fetch all biddings
@app.route('/products/biddings', methods=['GET','POST'])
def allbids():
    allb = Biddings.fetch_all()

    return render_template('bids.html', allb=allb)


# update product status
@app.route('/status/update/<int:id>', methods=['GET','POST'])
def update_status(id):
    if request.method == 'POST':
        newStatus = request.form['newstatus']
        up = Products.update_product_by_id(id=id,status=newStatus)

        if up:
            flash('update successful','success')
            return redirect(url_for('products_all'))
        else:
            flash('record not found','danger')
            return redirect(url_for('products_all'))

#delete a product
@app.route('/delete/<int:id>', methods=['POST']) 
def delete(id):
    deleted = Products.delete_by_id(id)
    if deleted:
        flash("Deleted Succesfully",'success')
        return redirect(url_for('products_all'))
    else:
        flash("Record not found",'danger')
        return redirect(url_for('products_all'))


# customer registration
@app.route('/registration', methods=['GET','POST'])
def customer_reg():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            confirmpass = request.form['confirmpass']

            if password != confirmpass:
                flash('Passwords dont match!','danger')
                return redirect(url_for('customer_reg'))
            elif(CustomerModel.check_email_exist(email)):
                flash('Email already in use','danger')
                return redirect(url_for('customer_reg'))
            else:
                # protect the password by harshing it
                hashedpass = bcrypt.generate_password_hash(password,10).decode('utf-8')
                # add the customer to the database
                customer = CustomerModel(name=name,email=email,phone_number=phone,password=hashedpass)
                customer.insert_record()

                flash('Your account has been successfully created.Please Login','success')
                return redirect(url_for('customer_login'))

        except Exception as e:
            print(e)

    return render_template('customerreg.html')

# customer login
@app.route('/login', methods=['GET','POST'])
def customer_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # check if an email exists
        if CustomerModel.check_email_exist(email=email):
            # validate the password
            if CustomerModel.validate_password(email=email,password=password):
                # set the customer session
                session['email'] = email
                session['uid'] = CustomerModel.get_customer_id(email)
                # redirect him to the homepage
                return redirect(url_for('home'))
            else:
                flash('Invalid login credential','danger')
                return redirect(url_for('customer_login'))
        else:
            flash('Invalid login credential', 'danger')
            return redirect(url_for('customer_login'))

    return render_template('custlogin.html')

# customer logout
@app.route('/cus/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

# auctioner logout
@app.route('/auc/logout', methods=['POST'])
def logout_auc():
    session.clear()
    return redirect(url_for('index'))


# customer homepage
@app.route('/customer', methods=['GET','POST'])
def home():
    # first check if a user session has been set
    if session:
        print(session)
        allProducts = Products.fetch_by_status_onsale()
        return render_template('home.html', allProducts=allProducts)
    else:
        # redirect the customer to the login page
        return redirect(url_for('customer_login'))






    






if __name__ == '__main__':
    app.run(port=5001,debug=True)