from flask import Flask,request,render_template,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
engine = create_engine('mysql://root:varunasd1@localhost/test')
app = Flask(__name__)
app.secret_key = 'my unobvious secret key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:varunasd1@localhost/test'
db = SQLAlchemy(app)   

requests = db.Table('requests',
	db.Column('id', db.Integer, db.ForeignKey('user.id')),
	db.Column('splreq_id' ,db.Integer, db.ForeignKey('splreq.splreq_id'))
	)

class user(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username= db.Column(db.String(30),unique=True,nullable=False)
	email = db.Column(db.String(50),unique=True,nullable=False)
	password = db.Column(db.String(50),nullable=False)
	owner = db.relationship("booking")
	complains = db.relationship("complains")
	requesting = db.relationship('splreq',secondary = requests)
	logis = db.relationship('logisreq',uselist=False)	

	def __init__(self, id, username, email, password):
		self.id = id
		self.username = username
		self.email = email
		self.password = password

permbook = db.Table('permbook',
	db.Column('booking_id', db.Integer, db.ForeignKey('booking.booking_id')),
	db.Column('perm_id' ,db.Integer, db.ForeignKey('perms.perm_id'))	
	)

class booking(db.Model):
	__tablename__ = 'booking'
	booking_id = db.Column(db.Integer, primary_key=True)
	event_name = db.Column(db.String(50),nullable=False)
	id = db.Column(db.Integer, db.ForeignKey('user.id'))
	room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'))
	bookings = db.relationship('perms',secondary = permbook)

class room(db.Model):
	__tablename__ = 'room'
	room_id = db.Column(db.Integer, primary_key=True)
	status = db.Column(db.Boolean,default=False)
	building = db.Column(db.String(10),nullable=False)

class perms(db.Model):
	__tablename__ = 'perms'
	perm_id = db.Column(db.Integer, primary_key=True)
	name= db.Column(db.String(100),nullable=False)
	reg= db.Column(db.Integer,unique=True,nullable=False)
	cgpa = db.Column(db.Numeric(2,2))
	timing = db.Column(db.Integer,nullable=False)
	start_date = db.Column(db.DateTime)
	end_time = created = db.Column(db.DateTime)
	gatepass = db.Column(db.Boolean,default=False)
	id = db.Column(db.Integer, db.ForeignKey('user.id'))
	#booking_id = db.Column(db.Integer, db.ForeignKey('booking.booking_id'))
	rid = db.Column(db.Integer, db.ForeignKey('ruser.rid'))


class complains(db.Model):
	__tablename__ = 'complains'
	complain_id = db.Column(db.Integer, primary_key=True)
	complain = db.Column(db.String(2000),nullable=False)
	id = db.Column(db.Integer, db.ForeignKey('user.id'))

class splreq(db.Model):
	__tablename__ = 'splreq'
	splreq_id = db.Column(db.Integer, primary_key=True)
	splreq = db.Column(db.String(2000),nullable=False)
	comment = db.Column(db.String(2000))
	#id = db.Column(db.Integer, db.ForeignKey('user.id'))
	adid = db.Column(db.Integer, db.ForeignKey('admin.aid'))
"""
class progress(db.Model):
	__tablename__ = 'progress'
	council = db.Column(db.Boolean,default=False)
	director = db.Column(db.Boolean,default=False)
	security = db.Column(db.Boolean,default=False)
	perm = db.Column(db.Boolean,default=False)
	booking_id = db.Column(db.Integer, db.ForeignKey('booking.booking_id'))
	#adid = db.Column(db.Integer, db.ForeignKey('admin.aid'))
"""
class admin(db.Model):
	__tablename__ = 'admin'
	aid = db.Column(db.Integer, primary_key=True)
	username= db.Column(db.String(30),unique=True,nullable=False)
	email = db.Column(db.String(50),unique=True,nullable=False)
	password = db.Column(db.String(50),nullable=False)
	role = db.Column(db.String(20),nullable=False)
	#auth = db.relationship('progress',userlist=False)
	request = db.relationship('splreq',uselist=False)

class ruser(db.Model):
	__tablename__ = 'ruser'
	rid = db.Column(db.Integer, primary_key=True)
	username= db.Column(db.String(30),unique=True,nullable=False)
	email = db.Column(db.String(50),unique=True,nullable=False)
	password = db.Column(db.String(50),nullable=False)
	role = db.Column(db.String(20),nullable=False)
	read = db.relationship("perms")

class logisreq(db.Model):
	__tablename__ = 'logisreq'
	items = db,Column(db.String(1000))
	id = db.Column(db.Integer,db.ForeignKey('user.id'), primary_key=True)

@app.route('/')
def showcase():
	return render_template('index.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/Wazza')
def Wazzaa():
	return "Hello World"



# @app.route('/index',methods=['GET','POST'])
# def index():
# 	#if request=="POST":
# 		#DEFINE registration that is putting username password in database



@app.route('/landing', methods=['GET','POST'] )
def land():
	res = ""
	t=0
	if request.method == "POST":
	  email =request.form["email"]
	  passw = request.form["password"]
	with engine.connect() as con:
  	  	rs = con.execute('SELECT email,password FROM user').fetchall()
  	  	for row in rs:
  	  		print(rs[0])
  	  		if email == row[0] and passw == row[1]:
  	  			t=1
  	  			break
	if t == 0:
	  flash('Invalid user credentials')
	  return render_template('login.html')
	else:
	  flash(email)
	  return render_template('user_home.html')

# @app.route('/permi',methods=['GET','POST'])
# def permi():
# 	if request.method=='POST'
	# put all the fields from the form in the table	  	

# @app.route('/reqi',methods=['GET','POST'])
# def permi():
# 	if request.method=='POST'
# 	# put all the fields from the form in the table	 	

@app.route('/register',methods=['GET','POST'])
def register():
	return render_template('register.html')

@app.route('/user_home',methods=['GET','POST'])
def user_home():
	flash(' Leaders of tomorrow ')
	return render_template('user_home.html')

@app.route('/building',methods=['GET','POST'])
def building():
	return render_template('building.html')

@app.route('/status',methods=['GET','POST'])
def status():
	return render_template('status.html')

@app.route('/requestt',methods=['GET','POST'])
def requestt():
	return render_template('request.html')

@app.route('/perm',methods=['GET','POST'])
def perm():
	return render_template('perm.html')


if __name__ == '__main__':
	app.config['SESSION_TYPE'] = 'filesystem'
	sess.init_app(app)
	app.debug = True
	app.run(host = '0.0.0.0',port =5000)

