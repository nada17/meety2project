from flask import Flask, url_for, flash, redirect, request, g
from databases import *
from flask import session as login_session
from passlib.apps import custom_app_context as pwd_context


app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"

# def verify_password(email, password):
# 	user = session.query(User).filter_by(email=email).first()
# 	if not user or not user.verify_password(password):
# 		return False
# 	g.user = user
# 	return True
	
def verify_password(email, password1):
	user = session.query(User).filter_by(email=email).first()
	if user.hash_password(password1) == user.password and user is not None:
		return True
	return False

# def hash_password(password):
# 	return pwd_context.encrypt(password)



@app.route('/')
def world():
	return render_template('home.html')
@app.route('/home')
def home():
	items = session.query(Book).all()
	print ("home")
	return render_template('home.html', items = items)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	if request.method == 'POST':
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		email = request.form['email']
		password = request.form['password']
		confirmpassword = request.form['confirmpassword']
		imgurluser = request.form['imgurluser']
		dob = request.form['dob']
		phonenumber = request.form['phonenumber']
		if firstname == "" or lastname == "" or email == "" or password == "" or confirmpassword == "" or dob == "" or phonenumber == "":
			flash("Your form is missing arguments")
			return redirect(url_for('signup'))
		if session.query(User).filter_by(email=email). first() is not None:
			flash("A user with this email address already exists")
			return redirect(url_for('signup')) 
		user = User(firstname=firstname,lastname=lastname, email=email, imgurluser=imgurluser, dob=dob, phonenumber=phonenumber)
		user.hash_password(password)
		session.add(user)
		session.commit()
		flash("User created successfully")
		return redirect(url_for('login'))
	else:
		return render_template('signup.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if email == "" or password == "":
			flash("Missing Arguements")
			return redirect(url_for('login'))

		user = session.query(User).filter_by(email=email).first()
		if not user:
			flash("Incorrect password / email combination")
			return redirect(url_for('login'))
		elif verify_password(user.email, password): 
			flash('Login Successful. Welcome, %s' %user.firstname)
			login_session['firstname']= user.firstname
			login_session['lastname'] = user.lastname
			login_session['email'] = user.email
			print("LogIn")
			login_session['id'] = user.id
			return redirect(url_for('home'))
		

@app.route('/newbook', methods=['GET', 'POST'])
def newbook():
	if request.method == 'POST':
		title = request.form['title']
		author = request.form['author']
		pubyear = request.form['pubyear']
		imgurlbook = request.form['imgurlbook']
		genre = request.form['genre']
		location = request.form['location']
		if title == "" or author == "" or pubyear == "" or genre == "" or location == "":
			flash("Your form is missing arguements")
			return redirect(url_for('newbook'))
		book = Book(title=title, author=author, pubyear=pubyear, imgurlbook=imgurlbook, genre=genre, location=location)
		session.add(book)
		session.commit()
		flash("Book added successfully!")
		return redirect(url_for('home'))
	else:
		return render_template('newbook.html')



@app.route('/user/<email>')
def user_profile(user_email):
	user_email = session.query(User).filter_by(email).first(user_email=user_email)
	return render_template('user.html', user_email=user_email)




@app.route('/book/<int:book_id>')
def book (book_id):
	book = session.query(Book).filter_by(id=book_id).one()
	return render_template('home.html', book=book)



@app.route('/logout', methods = ['POST'])
def logout():
	if 'id' not in login_session:
		flash("You must be logged in order to log out")
		return redirect(url_for('login'))
	del login_session['firstname']
	del login_session['lastname']
	del login_session['email']
	del login_session['id']
	flash("Logged out successfully")
	return redirect(url_for('home'))





if __name__ == '__main__':
	app.run(debug=True)