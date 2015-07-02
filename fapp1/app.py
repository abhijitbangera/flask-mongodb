from flask import Flask, render_template,url_for,request,redirect,session,flash
from functools import wraps
from pymongo import MongoClient
import os

#DB connection


app=Flask(__name__)

app.secret_key="abhijitkey3"

def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('you need to login first')
			return redirect(url_for('login'))
	return wrap

@app.route('/')
@login_required
def home():
	user=session['key']
	return render_template("index.html",user=user)

@app.route('/welcome')
def welcome():
	return render_template("welcome.html")

@app.route('/profile/<username>')
@login_required
def user_profile(username):
	if session['logged_in']!=True:
		return redirect("/")
	else:
		user = people.find_one({'name': username})
		print(user)
		if username!=session['key']:
			user1="You are not authorized"
			print(user1)
		else:
		    
		    print("user is:")
		    print(user['name'])
		    print("pass is:")
		    print(user['pass'])
		    user1 = user
	return render_template('userprofile.html', user=user1)
@app.route('/update/',methods=['GET', 'POST'])
@login_required
def update():
	if request.method=="POST":
		# user = people.find_one({'name': request.form['username']})
		if request.form['age']!="" or request.form['country']!="":
			print("updating..")
			people.update( {'name':session['key']}, { "$set":{ "age": request.form['age'], "country": request.form['country']}} ) 
			return redirect(url_for('update_success'))
	else:
		print("update failed")
	return render_template("updated.html")

@app.route('/updatesucess/')
@login_required
def update_success():
	message="Update was successful"
	peeps=people.find()
	print ("searching")
	for person in peeps:
		print(person)
	print(session['key'])
	user = people.find_one({'name': session['key']})
	print("user is:" )
	print( user)
	return render_template('updated.html', user=user)





@app.route('/user/login',methods=['GET','POST'])
def login():
	error=None
	try:
		if session['logged_in']==True:
			return redirect("/")
	except:
		if request.method=='POST':
			try:
				user = people.find_one({'name': request.form['username']})
				if request.form['username']!=user['name'] or request.form['password']!=user['pass']:
				# if request.form['username']!='admin' or request.form['password']!='admin':
					error='Invalid credentials. Please try again'
				else:
					session['logged_in']=True
					session['key']=request.form['username']
					flash('you are logged in')
					return redirect('/profile/'+user['name'])
					# return redirect(url_for('user_profile'),username='1')
			except:
				error='Invalid credentials. Please try again'
	return render_template('login.html',error=error)

@app.route('/user/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	flash('you are logged out')
	app.secret_key = os.urandom(32)
	# response.headers['Cache-Control'] = 'no-cache'
	return redirect(url_for('welcome'))

# @app.route('/user/<username>')
# def user_profile(username):
#     user = people.findone({'_name': username})
#     return render_template('user.html',
#         user=user)





@app.route('/user/signup', methods=['GET', 'POST'])
def register():
	if request.method=="POST":
		if (request.form['username'])!="" or (request.form['password'])!="":
			print("something")
			people.insert({'name':request.form['username'],'pass':request.form['password'],'email':'','country':''})
			peeps=people.find()
			print ("insert and find")
			for person in peeps:
				print(person)
			return redirect(url_for('login'))
		else:
			print("nothing")

	print("123")
	return render_template('register.html')


if __name__=='__main__':
	con=MongoClient()
	db=con.test_database
	people=db.people
	# insrt1=people.insert({'name':'abhi','pass':'123'})
	# insrt1
	peeps=people.find()
	print ("insert and find")
	for person in peeps:
		print(person)
	
	
	app.run(debug=True)
