from flask import Flask, url_for, flash, redirect, request, g
from databases import *
from flask import session as login_session

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"

def verify_password(email, password):
	user = session.query(user).filter_by(email=email).first()
	if not user or not customer.verify_password(password):
		return False
	return False


@app.route('/')
def world():
	return "zidane sucks"
@app.route('/home/')
def home():
	items = session.query(books).all()
	return render_template('inventory.html', items = items)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	if request.method == 'POST':
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		email = request.form['email']
		password = request.form['password']
		imgurluser = request.form['imgurluser']
		dob = request.form['dob']
		phonenum = request.form['phonenumber']
		if firstname == "" or lastname == "" or email == "" or password == "" or dob == "" or phonenumber == "":
			flash("Your form is missing arguments")
			return redirect(url_for('signup'))
		if session.query(user).filter_by(email=email). first() is not None:
			flash("A user with this email address already exists")
			return redirect(url_for('signup'))
		user = user(firstname=firstname,lastname=lastname, email=email, dob=dob, phonenumber=phonenumber)
		user.hash_password(password)
		session.add(user)
		session.commit()
		flash("User created successfully")
		return redirect(url_for('home'))
	else:
		return render_template('signup')




@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		email=request.form['email']
		password = request.form['password']
		if email is None or password is None:
			flash("Missing Arguements")
			return redirect(url_for('login'))
		if verify_password(email, password):
			user = session.query(users).filter_by(email=email).one()
			flash('Login Successful. Welcome, %s' %user.firstname)
			login_session['firstname']= user.firstname
			login_session['lastname'] = user.lastname
			login_session['email'] = user.email
			login_session['id'] = user.id
			return redirect(url_for('inventory'))
		else:
			flash('Incorrect email/password combination')
			return redirect(url_for('login'))

@app.route('/newbook')
def newbook():
	if request.form == 'POST':
		title = request.form['title']
		author = request.form['author']
		pubyear = request.form['pubyear']
		imgurlbook = request.form['imgurlbook']
		genre = request.form['genre']
		location = request.form['location']
		if title == "" or author == "" or pubyear == "" or genre == "" or location == "":
			flash("Your form is missing arguements")
			return redirect(url_for('newbook'))
		book = book(title=title, author=author, pubyear=pubyear, imgurlbook=imgurlbook, genre=genre, location=location)
		session.add(book)
		session.commit()
		flash("Book added successfully!")
		return redirect(url_for('newbook'))
	else:
		return render_template('newbook.html')



@app.route('/user/<username>')
def user_profile(username):
	return "lol"


@app.route('/book/<int:book_id>')
def book (book_id):
	book = session.query(books).filter_by(id=book_id).one()
	return render_template('inventory.html', book=book)



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
	return redirect(url_for('inventory'))





if __name__ == '__main__':
	app.run(debug=True)