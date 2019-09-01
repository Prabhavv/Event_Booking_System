from flask import Flask,request,render_template,flash,redirect,url_for
app = Flask(__name__)
app.secret_key = 'my unobvious secret key'

@app.route('/')
def showcase():
	return render_template('index.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/Wazza')
def Wazzaa():
	return "Hello World"

@app.route('/landing', methods=['GET','POST'] )
def land():
	res = ""
	if request.method == "POST":
	  email =request.form["email"]
	  passw = request.form["password"]
	  flash('Wazza matey')
	  return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
	return render_template('register.html')




if __name__ == '__main__':
	app.config['SESSION_TYPE'] = 'filesystem'
	sess.init_app(app)
	app.debug = True
	app.run(host = '0.0.0.0',port =5000)
