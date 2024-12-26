import re
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
import uuid
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
import os
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, current_user, login_required, login_user, LoginManager, logout_user
from flask_bcrypt import Bcrypt
from datetime import datetime
#import psycopg2 

app = Flask(__name__, template_folder='templates')

app.config[ 'SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:HAYAstan@Localhost:5432/car"
app.config['SECRET_KEY'] = os.urandom(32)
app.config [' SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)					
migrate = Migrate(app, db)

with app.app_context() :
	db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = 'Вы не можете получить достул к данной странице• Нужно сначала войти'

@login_manager.user_loader 
def load_user(user_id):
	return Users.query.get(user_id) 

class Client (db.Model, UserMixin):
	id = db.Column (db.Text, primary_key=True)
	name = db.Column (db.Text (50))
	phone_number = db.Column (db.Text (50))

class RegistrationForm(FlaskForm) :
	login = StringField('Логин', validators= [DataRequired(), Length (min=2, max=20)]) 
	password = PasswordField('Пароль', validators= [DataRequired(), Length (min=2, max=20)])
	confirm_password = PasswordField ( 'Подтвердите пароль', validators= [DataRequired(), EqualTo('password') ]) 
	submit = SubmitField ('Зарегистрироваться')

class Seller (db.Model, UserMixin):
	id = db.Column (db.Text, primary_key=True)
	login = db.Column (db.Text (50))
	password = db.Column (db.Text (200))

class Users (db.Model, UserMixin):
	id = db.Column (db.Integer, primary_key=True)
	login = db.Column (db.Text (50))
	password = db.Column (db.Text (200))
	role = db.Column(db.String(50))

class Products(db.Model):
	id = db.Column(db.Text, primary_key=True)
	name = db.Column (db.Text, nullable=False)
	count = db.Column (db.Integer, nullable=False)
	cost = db.Column (db.Integer, nullable=False)

class Orders (db.Model, UserMixin):
	id = db.Column (db.Integer, primary_key=True)
	created_at = db.Column (db.Text (50))
	client_id = db.Column (db.Text (200))
	product_name = db.Column(db.String(50))

class LoginForm(FlaskForm): 
	login = StringField('Логин', validators= [DataRequired(), Length (min=2, max=20)]) 
	password = PasswordField('Пароль', validators= [DataRequired()]) 
	submit = SubmitField ('Войти')

@app.route('/index')
@app.route('/') 
def index(): 
	return render_template('index.html') 

@app.route('/create', methods=['POST', 'GET'])
@login_required
def create(): 
	if current_user.role == 'admin':
		if request.method == 'POST':
			name = request.form.get('product_name')
			count = request.form.get('count')
			cost = request.form.get('cost')

			if name not in ("Playstation5 Slim", "Playstation5 Slim Digital Edition", "Playstation5 Pro", "Playstation5 Pro Digital Edition", "Xbox Series S", "Xbox Series X", "Xbox Wireless Controller", "DualSense", "Nintendo Switch Pro Controller"):
				flash(f"Введите корректное название модели. Возможно вы ввели с маленькой буквы или кирилицой", "danger")
				return render_template('create.html')			

			products = Products(id=str(uuid.uuid4()), name=name, count=count, cost=cost)
			try:
				db.session.add(products)
				db.session.commit()
				return redirect('/')
			except Exception as e:
				print(f"error - {str(e)}")
				return 'Обосрался'
		else:
			return render_template('create.html')
	else:
		flash(f"У вас нет доступа к этой странице!", "danger")
		return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
	bcrypt = Bcrypt()
	
	form = LoginForm ()
	if form.validate_on_submit():
		user = Users.query.filter_by(login=form.login.data).first()
		
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			
			next_page = request.args.get ('next')
			
			return redirect(next_page) if next_page else redirect('/')		
	
	return render_template('login.html', form=form)

@app.route ('/register', methods=[ 'POST', 'GET']) 
def register():
	bcrypt = Bcrypt()

	form = RegistrationForm()
	if form.validate_on_submit():
		try:
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode ('utf-8')		
			user = Users(id=str(uuid.uuid4()), login=form.login.data, password=hashed_password, role='user')
			
			db.session.add(user)
			db.session.commit()

			return redirect('/login')
		except Exception as e:
			print(f"error - {str(e)}")
			flash(f"Ошибка регистрации!", "danger")
			return render_template('register.html', form=form)
	
	return render_template('register.html', form=form)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
	logout_user()
	return redirect('/')

@app.route('/Xbox')
def Xbox(): 
	return render_template('Xbox.html') 

@app.route('/Playstation')
def Playstation(): 
	return render_template('Playstation.html') 

@app.route('/Nintendo')
def Nintendo(): 
	return render_template('Nintendo.html') 

@app.route('/Gamepads')
def Gamepads(): 
	return render_template('Gamepads.html') 

def is_valid_phone_number(phone_number):
    pattern = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
    return bool(re.match(pattern, phone_number))

@app.route('/deal', methods=['POST', 'GET'])
@login_required
def deal():	
	if request.method == 'POST':
		name = request.form.get('name')
		phone_number = request.form.get('phone_number')
		product_name = request.form.get('product_name')

		if not (is_valid_phone_number(phone_number)):
			flash(f"Введите корректный номер телефона", "danger")
			return render_template('deal.html')

		if product_name not in ("Playstation5 Slim", "Playstation5 Slim Digital Edition", "Playstation5 Pro", "Playstation5 Pro Digital Edition", "Xbox Series S", "Xbox Series X", "Xbox Wireless Controller", "DualSense", "Nintendo Switch Pro Controller"):
			flash(f"Введите корректное название модели. Возможно вы ввели с маленькой буквы или кирилицой", "danger")
			return render_template('deal.html')

		
		product = Products.query.filter_by(name=product_name).first()
		if product:
			orders = Orders.query.filter_by(client_id=current_user.id).first()
			if orders:			
				orders.product_name = orders.product_name + " " + product_name
				#car.count = car.count - 1
				try:
					db.session.commit()

					flash(f"Вы изменили заказ, для уточнения комплектации свяжитесь с нами по номеру или приезжайете в наш автосалон по адресу:... корпус 2.\nМы работаем с 10:00-22:00 каждый день", "success")
					return redirect('/')
				except Exception as e:
					print(f"error - {str(e)}")
					flash(f"Не удалось обновить заказ", "danger")
					return render_template('deal.html')

			client = Client(id=current_user.id, name=name, phone_number=phone_number)
			orders = Orders(id=str(uuid.uuid4()), created_at=datetime.now(), client_id=current_user.id, product_name=product_name)
			#car.count = car.count - 1
			try:
				db.session.add(client)
				db.session.add(orders)
				db.session.commit()

				#car.count = car.count - 1

				flash(f"Вы оформили заказ, для уточнения комплектации свяжитесь с нами по номеру или приезжайете в наш автосалон по адресу:...\nМы работаем с 10:00-22:00 каждый день", "success")
				return redirect('/')
			except Exception as e:
				print(f"error - {str(e)}")
				flash(f"Что-то пошло не так", "danger")
				return render_template('deal.html')
		else:
			flash(f"К сожалению этой машины сейчас нет в наличии", "danger")
			return render_template('deal.html')
	else:
		return render_template('deal.html') 

@app.route('/deals')
@login_required
def deals(): 
	if current_user.role == 'admin':
		order = Orders.query.all() 
		return render_template('deals.html', order=order) 
	else:
		order = Orders.query.filter_by(client_id=current_user.id).all()
		return render_template('deals.html', order=order)


if __name__ == '__main__': 
	app.run(debug=True) 


