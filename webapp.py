from flask import Flask, url_for, flash, redirect, request
from databases import *

app = Flask(__name__)

@app.route('/')
def world():
	return "Hilol"
@app.route('/home/')
def home():
	return "yay"

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	if request.method == 'POST':
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		email = request.form['email']
		password = request.form['password']
		image = request.form['img']
		dob = request.form['dob']
		phonenum = request.form['phonenumber']
		if firstname == "" or lastname == "" or email == "" or password == "" or dob == "" or phonenumber == "":
			flash("Your form is missing arguments")
			return redirect(url_for('signup.html'))
		if session.query(user).filter_by(email=email). first() is not None:
			flash("A user with this email address already exists")
			return redirect(url_for('signup.html'))
		user = user(firstname=firstname,lastname=lastname, email=email, dob=dob, phonenumber=phonenumber)
		user.hash_password(password)
		session.add(user)
		session.commit()
		flash("User created successfully")
		return redirect(url_for('home'))
	else:
		return render_template('signup.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
	return "lul"

@app.route('/book/<int:product_id>')
def book (book_id):
	return "lul"
@app.route('/logout', methods = ['POST'])
def logout():
	return "lul"

if __name__ == '__main__':
	app.run(debug=True)