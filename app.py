from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from wtforms import SelectField, IntegerField, StringField, FloatField, SubmitField, FileField, BooleanField, DateField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
import os
import uuid as uuid
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import subprocess

#create flask instance
app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/furniture_db"
app.config['SECRET_KEY'] = "abcdefg"

#initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

#saving image
user_upload_folder = 'static/img/upload/profile'
material_upload_folder = 'static/img/upload/material'
product_upload_folder = 'static/img/upload/product'

#save new image directory
def save_new_image(folder,form):
    app.config['UPLOAD_FOLDER'] = folder
    #generate a secure filename
    image_filename = secure_filename(form.image.data.filename)
    #set uuid
    image_name = str(uuid.uuid1()) + "_" + image_filename
    #saving image
    saver = request.files['image']
    saver.save(os.path.join(app.config['UPLOAD_FOLDER'],image_name))
    #set new filename to db
    form.image = image_name
    return image_name

#update image directory
def update_image(folder,query):
    app.config['UPLOAD_FOLDER'] = folder
    #generate a secure filename
    image_filename = secure_filename(query.image.filename)
    #set uuid
    image_name = str(uuid.uuid1()) + "_" + image_filename
    #saving image
    saver = request.files['image']
    saver.save(os.path.join(app.config['UPLOAD_FOLDER'],image_name))
    #set new filename to db
    query.image = image_name
    return image_name

#create model: Users
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    phone_num = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(300), nullable=False)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    image = db.Column(db.String(300))
    admin = db.Column(db.Boolean())
    access_right = db.Column(db.String(30))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    created_by = db.Column(db.Integer)
    modified_by = db.Column(db.Integer)

#create model: AccessRight
class AccessRight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_code = db.Column(db.String(30), nullable=False, unique=True)
    access_name = db.Column(db.String(300), nullable=False)
    access_desc = db.Column(db.String(300))

#access_right_list for access right SelectField
access_right_list=[]
for arl in AccessRight.query.all():
    index = 0
    access_right_list.insert(index, (arl.access_code,arl.access_name))
    index+=1  

#create model: StorageLocation
class StorageLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    storage_location_code = db.Column(db.String(30), nullable=False, unique=True)
    storage_location_name = db.Column(db.String(300), nullable=False)
    usable = db.Column(db.Boolean())
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def __repr__(self):
        return '{}'.format(self.storage_location_name)
    
#storage_loc_list for storage location SelectField
def storage_loc_list_query():
    storage_loc_list=[]
    for strl in StorageLocation.query.filter_by(usable=1):
        index = 0
        storage_loc_list.insert(index, (strl.storage_location_code,strl.storage_location_name))
        index+=1
    return storage_loc_list 

#create model: ProductMaterial (material_list and product_list relation table)
class ProductMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product_list.id'))
    material_id = db.Column(db.Integer, db.ForeignKey('material_list.id'))
    used_material_qty = db.Column(db.Integer)

#create model: MaterialList
class MaterialList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(30), nullable=False, unique=True)
    name = db.Column(db.String(300), nullable=False)
    qty = db.Column(db.Float)
    uom = db.Column(db.String(200), nullable=False)
    consumable = db.Column(db.Boolean())
    storage_location = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(300), nullable=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    created_by = db.Column(db.Integer)
    modified_by = db.Column(db.Integer)
    product_material = db.relationship('ProductMaterial', backref='product_materialer')

#create model: ProductList
class ProductList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_no = db.Column(db.String(30), nullable=False, unique=True)
    name = db.Column(db.String(300), nullable=False)
    qty = db.Column(db.Float)
    qty_uom = db.Column(db.String(200), nullable=False)
    weight = db.Column(db.Float)
    weight_uom = db.Column(db.String(200), nullable=False)
    storage_location = db.Column(db.String(200), nullable=False)
    currency = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(300), nullable=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    created_by = db.Column(db.Integer)
    modified_by = db.Column(db.Integer)
    producter = db.relationship('ProductMaterial', backref='producter')

#Form: UserForm
class UserForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    birth_date = DateField("Birth Date", validators=[DataRequired()])
    phone_num = StringField("Phone Number", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    username = StringField("Username",validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    admin = BooleanField("Grant Admin Rights")
    access_right = SelectField('Access Right to...', choices = access_right_list)
    image = FileField('Profile Picture')
    del_image = BooleanField('Turn this switch on to Delete Image')
    submit = SubmitField("Save")

#Form: LoginForm
class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

#Form: StorageLocationForm
class StorageLocationForm(FlaskForm):
    storage_location_code = StringField("Str loc. Code",validators=[DataRequired()])
    storage_location_name = StringField("Str loc. Name",validators=[DataRequired()])
    usable = BooleanField('Usable?')
    
    submit = SubmitField("Submit")

#Form: MaterialForm
class MaterialForm(FlaskForm):
    barcode = StringField("Barcode",validators=[DataRequired()])
    name = StringField("Material Name",validators=[DataRequired()])
    qty = FloatField("Quantity", default=0)
    uom = SelectField(u'Unit of Measure', choices=[('box','Box'),('pk','Pack'),('pc','Piece'), ('ton','Ton'), ('lbs', 'Pound'), ('m', 'Meter'), ('cm', 'Centimeter'), ('kg', 'Kilogram'), ('gr', 'Gram'), ('l', 'Liter'), ('ml', 'Mililiter'), ('rim', 'RIM'), ('etc', 'Other')])
    consumable = BooleanField('Consumable?')
    storage_location = SelectField('Storage Location', choices=storage_loc_list_query())
    image = FileField('Item image')
    del_image = BooleanField('Turn this switch on to Delete Image')
    submit = SubmitField("Save")    

#Form: ProductForm
class ProductForm(FlaskForm):
    model_no = StringField("Model No.",validators=[DataRequired()])
    name = StringField("Product Name",validators=[DataRequired()])
    qty = FloatField("Quantity", default=0)
    qty_uom = SelectField(u'Quantity UoM', choices=[('box','Box'),('pk','Pack'),('pc','Piece')])
    weight = IntegerField("Unit Weight",validators=[DataRequired()])
    weight_uom = SelectField(u'Unit Weight UoM', choices=[('kg','Kilogram'),('gr','Gram'),('ton','Ton'),('lbs','Pound')])
    storage_location = SelectField('Storage Location', choices=storage_loc_list_query())
    currency = SelectField(u'Currency', choices=[('IDR','Indonesian Rupiah'),('USD','United States Dollar'),('RMB','RMB Yuan')])
    price = FloatField('Base Price', validators=[DataRequired()])
    image = FileField('Item image')
    del_image = BooleanField('Turn this switch on to Delete Image')
    submit = SubmitField("Submit")


    
#create route decorator
@app.route('/', methods=['GET','POST'])
def index():
    form = LoginForm()
    #if user go to login page but already logged in, redirect to home page
    print(current_user.is_authenticated)
    if current_user.is_authenticated != False:
        return redirect(url_for('home'))
    #username and password check
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        #if user is exist in database
        if user:
            if user.password == form.password.data:
                login_user(user)
                flash(f"Welcome {user.name}!")
                my_user = Users.query.all()
                
                return redirect(url_for('home'))
            elif user.password != form.password.data:
                flash("You are type wrong password or username.")
            
        else:
            flash("You are type wrong username or password.")
    return render_template("index.html",page='Login Page', form=form)

#logout page
@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You logged out from this app.")
    return redirect(url_for('index'))

#home page
@app.route('/home', methods=['GET','POST'])
@login_required
def home():
    current_user_id = current_user.id
    active_user_id = None
    count_material = db.session.query(MaterialList.id).count()
    count_product = db.session.query(ProductList.id).count()
    my_users = Users.query.filter_by(id=current_user_id).first()
    return render_template("home.html",page='Home Page',count_material=count_material,count_product=count_product, my_users=my_users, id=current_user_id)

#manage_users page to manage user profile and right access
@app.route('/manage_users', methods=['GET','POST'])
@login_required
def manage_users():
    my_users = Users.query.order_by(Users.admin.desc())
    current_user_id = current_user.id
    active_user_id = Users.query.filter_by(id=current_user_id).first()
    if active_user_id.admin == 1:
        return render_template("manage_users.html", my_users=my_users, page='Manage Users')
    elif active_user_id.admin == 0:
        flash("You do not have right to access this page.")
        return redirect(url_for('home'))
    
#Create user
@app.route('/manage_users/create', methods=['GET','POST'])
def create_user():
    data='user'
    username = None
    form = UserForm()
    current_user_id = current_user.id
    active_user_id = Users.query.filter_by(id=current_user_id).first()

    #POST data
    if form.validate_on_submit():
        #user for checking username is already exist or not
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None:
            #if upload image
            if form.image.data:
                imagename=save_new_image(user_upload_folder,form)

                user = Users(name=form.name.data, 
                            birth_date=form.birth_date.data, 
                            phone_num=form.phone_num.data, 
                            address=form.address.data, 
                            username=form.username.data, 
                            password=form.password.data,
                            admin=form.admin.data,
                            access_right=form.access_right.data,
                            image=imagename, 
                            date_created = datetime.today(), 
                            date_modified = datetime.today(),
                            created_by = current_user_id,
                            modified_by = current_user_id)
            #else if not upload image
            else:
                user = Users(name=form.name.data, 
                            birth_date=form.birth_date.data, 
                            phone_num=form.phone_num.data, 
                            address=form.address.data, 
                            username=form.username.data, 
                            password=form.password.data,
                            admin=form.admin.data,
                            access_right=form.access_right.data,
                            image='N/A', 
                            date_created = datetime.today(), 
                            date_modified = datetime.today(),
                            created_by = current_user_id,
                            modified_by = current_user_id)

            db.session.add(user)
            db.session.commit()
            flash("New user successfuly created.")
            return redirect(url_for('manage_users'))
        
        elif user is not None:
            flash("Same username is already exist! Please input another username.")
            
        form.name.data = ''
        form.birth_date.data = ''
        form.address.data = ''
        form.phone_num.data = ''
        username=form.username.data
        form.password.data = ''

    #GET data
    if active_user_id.admin == 1:
        my_users = Users.query.all()
        return render_template("create_user.html",
                            data=data,
                            page='Register an Account',
                            form=form,
                            username=username,
                            my_users=my_users)
    elif active_user_id.admin == 0:
        flash("You do not have right to access this page.")
        return redirect(url_for('home'))
    
#edit_profile
@app.route('/manage_users/edit_profile/<int:id>', methods=['GET','POST'])
@login_required
def edit_profile(id):
    form = UserForm()
    edit_profile = Users.query.get_or_404(id)
    get_admin_users = Users.query.filter_by(admin=1).count()
    current_user_id = current_user.id
    active_user_id = Users.query.filter_by(id=current_user_id).first()
    created_by_user = Users.query.filter_by(id=edit_profile.created_by).first()
    modified_by_user = Users.query.filter_by(id=edit_profile.modified_by).first()

    if request.method == "POST":
        if active_user_id.admin == 1:
            edit_profile.name = request.form['name']
            edit_profile.birth_date = request.form['birth_date']
            edit_profile.phone_num = request.form['phone_num']
            edit_profile.address = request.form['address']
            edit_profile.username = request.form['username']
            edit_profile.password = request.form['password']
            
            edit_profile.access_right = request.form['access_right']
        
        try:
            if edit_profile.image != "N/A":
                if form.del_image.data == True:
                    os.remove(user_upload_folder+'/'+edit_profile.image)
                    edit_profile.image = 'N/A'
            
            if form.image.data != None and edit_profile.image == "N/A":
                edit_profile.image = request.files['image']
                update_image(user_upload_folder,edit_profile)
                
            elif form.image.data != None and edit_profile.image != "N/A":
                os.remove(user_upload_folder+'/'+edit_profile.image)
                edit_profile.image = request.files['image']
                update_image(user_upload_folder,edit_profile)
                
            edit_profile.date_modified = datetime.today()
            edit_profile.modified_by = current_user_id
            if form.admin.data == False and get_admin_users == 1 and edit_profile.admin == 1:
                flash("This operation is cannot be processed, at least there must be one user to be admin!")
                return redirect(url_for('manage_users'))
            else:
                edit_profile.admin = form.admin.data
                db.session.commit()
                flash("Profile saved.")
                if edit_profile is not None and active_user_id.admin == 1:
                    return redirect(url_for('manage_users'))
                elif edit_profile is not None and active_user_id.admin != 1:
                    return redirect(url_for('home'))
                return render_template("edit_profile.html",
                                    form=form,
                                    edit_profile=edit_profile,
                                    id=id,page='Edit a Profile',
                                    active_user_id=active_user_id
                                    )
            
        except:
            flash("Profile edit failed, error is occured.")
            return render_template("edit_profile.html",
                                form=form,
                                edit_profile=edit_profile,
                                id=id,page='Edit a Profile',
                                active_user_id=active_user_id)
    #GET
    else:
        if edit_profile.id == current_user_id or active_user_id.admin == 1:
            print(form.image.data)
            print(edit_profile.birth_date)
            form.birth_date.data = edit_profile.birth_date
            if edit_profile.admin == 1:
                form.admin.data = True
            form.access_right.data = edit_profile.access_right
            return render_template("edit_profile.html",
                                        form=form,
                                        edit_profile=edit_profile,
                                        id=id,page='Update a Profile',
                                        created_by_user=created_by_user,
                                        modified_by_user=modified_by_user,
                                        active_user_id=active_user_id,
                                        current_user_id=current_user_id)
        else:
            flash("You do not have right to do this operation.")
            return redirect(url_for('home'))
        
#Delete user
@app.route('/manage_users/delete/<int:id>')
@login_required
def delete_user(id):
    user_delete = Users.query.get_or_404(id)
    form = UserForm()
    my_users = Users.query.all()
    current_user_id = current_user.id
    active_user_id = Users.query.filter_by(id=current_user_id).first()

    if active_user_id.admin == 1:
        try:
            if user_delete.image != "N/A":
                os.remove(user_upload_folder+'/'+user_delete.image)
            db.session.delete(user_delete)
            db.session.commit()
            flash("User delete successful")
            if user_delete is not None:
                return redirect(url_for('manage_users'))
            return render_template("manage_users.html",
                                page='Delete a User',
                                form=form,
                                my_users=my_users)
        except:
            flash('Product delete failed, error is occured.')
            return render_template("manage_users.html",
                                page='Delete a User',
                                form=form,
                                my_users=my_users)
    else:
        flash("You do not have right to do this action.")  

#storage_location to show avaiable storage location in database
@app.route('/storage_location')
@login_required
def storage_location():
    current_user_id = current_user.id
    active_user_id = Users.query.filter_by(id=current_user_id).first()
    if active_user_id.admin == 1:
        all_storage_location = StorageLocation.query.order_by(StorageLocation.date_modified.desc())
    elif active_user_id.admin == 0:
        flash("You not have right to access this page")
        return redirect(url_for('home'))
    return render_template("storage_location.html",all_storage_location=all_storage_location,page='Storage Location')

#Create storage location
@app.route('/storage_location/create', methods=['GET','POST'])
def create_storage_location():
    data='storage_location'
    storage_location_code = None
    form = StorageLocationForm()
    current_user_id = current_user.id
    active_user_id = Users.query.filter_by(id=current_user_id).first()

    #POST data
    if form.validate_on_submit():
        #user for checking username is already exist or not
        storage_location = StorageLocation.query.filter_by(storage_location_code=form.storage_location_code.data).first()
        if storage_location is None:
            storage_location = StorageLocation(storage_location_code=form.storage_location_code.data, 
                        storage_location_name=form.storage_location_name.data, 
                        usable=form.usable.data,
                        date_created = datetime.today(), 
                        date_modified = datetime.today())

            db.session.add(storage_location)
            db.session.commit()
            flash("New storage location successfuly created.")
            return redirect(url_for('storage_location'))
        
        elif storage_location is not None:
            flash("Same username is already exist! Please input another username.")
            
        form.storage_location_code.data = ''
        form.storage_location_name.data = ''
        form.usable.data = False
        storage_location_code=form.storage_location_code.data

    #GET data
    if active_user_id.admin == 1:
        all_storage_location = StorageLocation.query.all()
        return render_template("create.html",
                            data=data,
                            page='Create New Storage Location',
                            form=form,
                            storage_location_code=storage_location_code,
                            all_storage_location=all_storage_location)
    elif active_user_id.admin == 0:
        flash("You do not have right to access this page.")
        return redirect(url_for('home'))

#update_storage_location
@app.route('/storage_location/update/<int:id>', methods=['GET','POST'])
@login_required
def update_storage_location(id):
    data = 'storage_location'
    form = StorageLocationForm()
    storage_location_update = StorageLocation.query.get_or_404(id)
    current_user_id = current_user.id
    active_user_id = Users.query.filter_by(id=current_user_id).first()

    if request.method == "POST":
        if active_user_id.admin == 1:
            storage_location_update.storage_location_code = request.form['storage_location_code']
            storage_location_update.storage_location_name = request.form['storage_location_name']
            storage_location_update.usable = form.usable.data
        
            try:
                storage_location_update.date_modified = datetime.today()
                db.session.commit()
                flash("Storage Location saved.")
                if storage_location_update is not None:
                    return redirect(url_for('storage_location'))
                return render_template("update.html",
                                    form=form,
                                    storage_location_update=storage_location_update,
                                    id=id,page='Edit a Storage Location',
                                    data=data,
                                    active_user_id=active_user_id
                                    )
                
            except:
                flash("Storage Location edit failed, error is occured.")
                return render_template("update.html",
                                    form=form,
                                    storage_location_update=storage_location_update,
                                    id=id,page='Edit a Storage Location',
                                    data=data,
                                    active_user_id=active_user_id)
    #GET
    else:
        if active_user_id.admin == 1:
            form.usable.data = storage_location_update.usable
            return render_template("update.html",
                                        form=form,
                                        storage_location_update=storage_location_update,
                                        id=id,page='Update a Profile',
                                        data=data,
                                        active_user_id=active_user_id,
                                        current_user_id=current_user_id)
        else:
            flash("You do not have right to do this operation.")
            return redirect(url_for('home'))
        
# Delete storage_location
@app.route('/storage_location/delete/<int:id>')
@login_required
def delete_storage_location(id):
    storage_location_delete = StorageLocation.query.get_or_404(id)
    form = StorageLocationForm()
    current_user_id = current_user.id
    active_user_id = Users.query.filter_by(id=current_user_id).first()

    if active_user_id.admin == 1:
        try:
            db.session.delete(storage_location_delete)
            db.session.commit()
            flash("Storage Location delete successful")
            if storage_location_delete is not None:
                return redirect(url_for('storage_location'))
            return render_template("storage_location.html",
                                page='Storage Location',
                                form=form)
        except:
            flash('storage_location_delete delete failed, error is occured.')
            return render_template("storage_location.html",
                                page='Delete a Storage Location',
                                form=form)
    else:
        flash("You do not have right to do this action.")  

# material to show material list from database
@app.route('/material')
@login_required
def material():
    current_user_id = current_user.id
    created_by_user = Users.query.filter_by(id=current_user_id).first()
    #check if user access right is ALL_CREATOR or ONLY_CREATOR
    if created_by_user.access_right == 'ALL_CREATOR':
        my_products = ProductList.query.order_by(ProductList.date_modified.desc())
        my_materials = MaterialList.query.order_by(MaterialList.date_modified.desc())
    elif created_by_user.access_right == 'ONLY_CREATOR':
        my_products = ProductList.query.filter_by(created_by = created_by_user.id).order_by(ProductList.date_modified.desc())
        my_materials = MaterialList.query.filter_by(created_by = created_by_user.id).order_by(MaterialList.date_modified.desc())
    return render_template("material_list.html",my_products=my_products,my_materials=my_materials,page='Material List')

#Create material
@app.route('/material/create', methods=['GET','POST'])
@login_required
def create_material():
    data='material'
    barcode = None
    form = MaterialForm()
    current_user_id = current_user.id

    #POST data
    if form.validate_on_submit():
        material = MaterialList.query.filter_by(barcode=form.barcode.data).first()
        if material is None and form.qty.data != 0:
            if form.image.data:
                imagename=save_new_image(material_upload_folder,form)

                material = MaterialList(barcode=form.barcode.data, 
                                               name=form.name.data, 
                                               qty=form.qty.data, 
                                               uom=form.uom.data, 
                                               consumable=form.consumable.data, 
                                               image=imagename, 
                                               storage_location=form.storage_location.data,
                                               date_created = datetime.today(), 
                                               date_modified = datetime.today(),
                                               created_by = current_user_id,
                                               modified_by = current_user_id)
            else:
                material = MaterialList(barcode=form.barcode.data, 
                                               name=form.name.data, 
                                               qty=form.qty.data, 
                                               uom=form.uom.data, 
                                               consumable=form.consumable.data, 
                                               image='N/A', 
                                               storage_location=form.storage_location.data,
                                               date_created = datetime.today(), 
                                               date_modified = datetime.today(),
                                               created_by = current_user_id,
                                               modified_by = current_user_id)

            db.session.add(material)
            db.session.commit()
            flash("New material successfuly created and saved.")
            return redirect(url_for('material'))
        elif material is not None:
            flash("Same material barcode is already exist! Please input barcode that not exist to create new material.")
            
        barcode=form.barcode.data
        form.barcode.data = ''
        form.name.data = ''
        form.qty.data = ''
        form.uom.data = ''
        form.consumable.data = False

    #GET data
    my_materials = MaterialList.query.all()
    form.storage_location.choices = storage_loc_list_query()
    return render_template("create.html",
                           data=data,
                           page='Create New Material',
                           form=form,
                           barcode=barcode,
                           my_materials=my_materials)

#Update material
@app.route('/material/update/<int:id>', methods=['GET','POST'])
@login_required
def update_material(id):
    data='material'
    form = MaterialForm()
    material_update = MaterialList.query.get_or_404(id)
    current_user_id = current_user.id
    active_user_id = Users.query.filter_by(id=current_user_id).first()
    created_by_user = Users.query.filter_by(id=material_update.created_by).first()
    modified_by_user = Users.query.filter_by(id=material_update.modified_by).first()
    
    #POST data
    if request.method == "POST":
        material_update.barcode = request.form['barcode']
        material_update.name = request.form['name']
        material_update.qty = request.form['qty']
        material_update.uom = request.form['uom']
        material_update.consumable = form.consumable.data
        material_update.storage_location = form.storage_location.data
        
        try:        
            if material_update.image != "N/A":
                if form.del_image.data == True:
                    os.remove(material_upload_folder+'/'+material_update.image)
                    material_update.image = 'N/A'
            
            if form.image.data != None and material_update.image == "N/A":
                material_update.image = request.files['image']
                update_image(material_upload_folder,material_update)
                
            elif form.image.data != None and material_update.image != "N/A":
                os.remove(material_upload_folder+'/'+material_update.image)
                material_update.image = request.files['image']
                update_image(material_upload_folder,material_update)
                
            material_update.date_modified = datetime.today()
            material_update.modified_by = current_user_id
            db.session.commit()
            flash("Material update successful")
            
            if material_update is not None:
                return redirect(url_for('material'))
            
            return render_template("update.html",
                                form=form,
                                material_update=material_update,
                                data=data,
                                id=id,page='Edit a Material',
                                created_by_user=created_by_user
                                )
            
        except:
            flash("Material update failed, error is occured.")
            return render_template("update.html",
                                form=form,
                                material_update=material_update,
                                data=data,
                                id=id,page='Update a Material',
                                created_by_user=created_by_user)
    #GET data
    else:
        #access right check
        if material_update.created_by != current_user_id and active_user_id.access_right == 'ONLY_CREATOR' and active_user_id.admin != 1:
            flash("You do not have right to operate this action.")
            return redirect(url_for('home'))
        elif material_update.created_by == current_user_id or active_user_id.access_right == 'ALL_CREATOR' or active_user_id.admin == 0:
            form.uom.data = material_update.uom
            form.storage_location.choices = storage_loc_list_query()
            form.storage_location.data = material_update.storage_location
            if material_update.consumable == 1:
                form.consumable.data = True
            
            return render_template("update.html",
                                    form=form,
                                    material_update=material_update,
                                    data=data,
                                    id=id,page='Update a Material',
                                    created_by_user=created_by_user,
                                    modified_by_user=modified_by_user)
        
#Delete material
@app.route('/material/delete/<int:id>')
@login_required
def delete_material(id):
    data='material'
    material_delete = MaterialList.query.get_or_404(id)
    barcode = None
    form = MaterialForm()
    my_materials = MaterialList.query.all()
    current_user_id = current_user.id
    active_user_id = Users.query.filter_by(id=current_user_id).first()

    if my_materials.created_by != current_user_id and active_user_id.access_right == 'ONLY_CREATOR' and active_user_id.admin != 1:
        flash("You do not have right to operate this action.")
        return redirect(url_for('home'))
    elif my_materials.created_by == current_user_id or active_user_id.access_right == 'ALL_CREATOR' or active_user_id.admin == 1:
        try:
            if material_delete.image != "N/A":
                os.remove(material_upload_folder+'/'+material_delete.image)
            db.session.delete(material_delete)
            db.session.commit()
            flash("Material delete successful")
            if material_delete is not None:
                return redirect(url_for('material'))
            return render_template("material_list.html",
                                data=data,
                                page='Delete a Material',
                                form=form,
                                barcode=barcode,
                                my_materials=my_materials)
        except:
            flash('Material delete failed, error is occured.')
            return render_template("material_list.html",
                                data=data,
                                page='Delete a Material',
                                form=form,
                                barcode=barcode,
                                my_materials=my_materials)

#product to show product list from database
@app.route('/product')
@login_required
def product():
    current_user_id = current_user.id
    created_by_user = Users.query.filter_by(id=current_user_id).first()
    if created_by_user.access_right == 'ALL_CREATOR':
        my_products = ProductList.query.order_by(ProductList.date_modified.desc())
        my_materials = MaterialList.query.order_by(MaterialList.date_modified.desc())
    elif created_by_user.access_right == 'ONLY_CREATOR':
        my_products = ProductList.query.filter_by(created_by = created_by_user.id).order_by(ProductList.date_modified.desc())
        my_materials = MaterialList.query.filter_by(created_by = created_by_user.id).order_by(MaterialList.date_modified.desc())
    
    return render_template("product_list.html",my_products=my_products,my_materials=my_materials,page='Product List')

#Create product
@app.route('/product/create', methods=['GET','POST'])
@login_required
def create_product():
    data='product'
    model_no = None
    form = ProductForm()
    current_user_id = current_user.id

    #POST data
    if form.validate_on_submit():
        product = ProductList.query.filter_by(model_no=form.model_no.data).first()
        #if same product query not found
        if product is None and form.qty.data != 0:
            #if image selected
            if form.image.data:
                imagename=save_new_image(product_upload_folder,form)

                product = ProductList(model_no=form.model_no.data, 
                                      name=form.name.data, 
                                      qty=form.qty.data, 
                                      qty_uom=form.qty_uom.data, 
                                      weight=form.weight.data, 
                                      weight_uom=form.weight_uom.data, 
                                      storage_location=form.storage_location.data,
                                      currency=form.currency.data,
                                      price=form.price.data,
                                      image=imagename, 
                                      date_created = datetime.today(), 
                                      date_modified = datetime.today(),
                                      created_by = current_user_id,
                                      modified_by=current_user_id)
            #if image not selected
            else:
                product = ProductList(model_no=form.model_no.data, 
                                      name=form.name.data, 
                                      qty=form.qty.data, 
                                      qty_uom=form.qty_uom.data, 
                                      weight=form.weight.data, 
                                      weight_uom=form.weight_uom.data, 
                                      storage_location=form.storage_location.data, 
                                      currency=form.currency.data,
                                      price=form.price.data,
                                      image='N/A', 
                                      date_created = datetime.today(), 
                                      date_modified = datetime.today(),
                                      created_by = current_user_id,
                                      modified_by = current_user_id)

            db.session.add(product)
            db.session.commit()
            flash("New product successfuly created and saved.")
            return redirect(url_for('product'))
        #if same product query found
        elif product is not None:
            flash("Same product model_no is already exist! Please input model_no that not exist to create new product.")
      
        model_no=form.model_no.data
        form.model_no.data = ''
        form.name.data = ''
        form.qty.data = 0
        form.qty_uom.data = ''
        form.weight.data = ''
        form.weight_uom.data = ''
        form.currency.data = ''
        form.price.data = 0
    #GET data
    my_products = ProductList.query.all()
    form.storage_location.choices = storage_loc_list_query()
    return render_template("create.html",
                           data=data,
                           page='Create New Product',
                           form=form,
                           model_no=model_no,
                           my_products=my_products)

#Update product
@app.route('/product/update/<int:id>', methods=['GET','POST'])
@login_required
def update_product(id):
    data='product'
    form = ProductForm()
    product_update = ProductList.query.get_or_404(id)
    current_user_id = current_user.id
    active_user_id = Users.query.filter_by(id=current_user_id).first()
    created_by_user = Users.query.filter_by(id=product_update.created_by).first()
    modified_by_user = Users.query.filter_by(id=product_update.modified_by).first()
    
    if request.method == "POST":
        product_update.model_no = request.form['model_no']
        product_update.name = request.form['name']
        product_update.qty = request.form['qty']
        product_update.qty_uom = request.form['qty_uom']
        product_update.weight = request.form['weight']
        product_update.weight_uom = request.form['weight_uom']
        product_update.storage_location = request.form['storage_location']
        product_update.currency = request.form['currency']
        product_update.price = request.form['price']
        
        try:
            if product_update.image != "N/A":
                if form.del_image.data == True:
                    os.remove(product_upload_folder+'/'+product_update.image)
                    product_update.image = 'N/A'
            
            if form.image.data != None and product_update.image == "N/A":
                product_update.image = request.files['image']
                update_image(product_upload_folder,product_update)
                
            elif form.image.data != None and product_update.image != "N/A":
                os.remove(product_upload_folder+'/'+product_update.image)
                product_update.image = request.files['image']
                update_image(product_upload_folder,product_update)
                
            product_update.date_modified = datetime.today()
            product_update.modified_by = current_user_id
            db.session.commit()
            flash("Product update successful")
            
            if product_update is not None:
                return redirect(url_for('product'))
            
            return render_template("update.html",
                                form=form,
                                product_update=product_update,
                                data=data,
                                id=id,page='Edit a Product'
                                )
            
        except:
            flash("Product update failed, error is occured.")
            return render_template("update.html",
                                form=form,
                                product_update=product_update,
                                data=data,
                                id=id,page='Update a Product')
        
    else:
        #access right check
        if product_update.created_by != current_user_id and active_user_id.access_right == 'ONLY_CREATOR' and active_user_id.admin != 1:
            flash("You do not have right to operate this action.")
            return redirect(url_for('home'))
        elif product_update.created_by == current_user_id or active_user_id.access_right == 'ALL_CREATOR' or active_user_id.admin == 1:
            print(form.image.data)
            form.storage_location.choices = storage_loc_list_query()
            form.qty_uom.data = product_update.qty_uom
            form.storage_location.data = product_update.storage_location
            form.currency.data = product_update.currency
            return render_template("update.html",
                                    form=form,
                                    product_update=product_update,
                                    data=data,
                                    id=id,page='Update a Product',
                                    created_by_user=created_by_user,
                                    modified_by_user=modified_by_user)

#Delete product
@app.route('/product/delete/<int:id>')
@login_required
def delete_product(id):
    data='product'
    product_delete = ProductList.query.get_or_404(id)
    model_no = None
    form = ProductForm()
    current_user_id = current_user.id
    my_product = ProductList.query.filter_by(id=current_user_id).first()
    active_user_id = Users.query.filter_by(id=current_user_id)

    if my_product.created_by != current_user_id and active_user_id.access_right == 'ONLY_CREATOR' and active_user_id.admin != 1:
        flash("You do not have right to operate this action.")
        return redirect(url_for('home'))
    elif my_product.created_by == current_user_id or active_user_id.access_right == 'ALL_CREATOR' or active_user_id.admin == 1:
        try:
            if product_delete.image != "N/A":
                os.remove(product_upload_folder+'/'+product_delete.image)
            db.session.delete(product_delete)
            db.session.commit()
            flash("Product delete successful")
            if product_delete is not None:
                return redirect(url_for('product'))
            return render_template("product_list.html",
                                data=data,
                                page='Delete a product',
                                form=form,
                                model_no=model_no,
                                my_products=my_products)
        except:
            flash('Product delete failed, error is occured.')
            return render_template("product_list.html",
                                data=data,
                                page='Delete a product',
                                form=form,
                                model_no=model_no,
                                my_products=my_products)



if __name__ == '__main__':
    app.run(debug=True)
