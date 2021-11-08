from flask import render_template, request, redirect, url_for, flash, session
import psycopg2
import psycopg2.extras
import requests
from app import app, db
from .forms import LoginForm, RegisterForm, BuyForm
from .models import Books, User, Cart
from flask_login import login_user, current_user, logout_user, login_required


def mergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    buy = BuyForm()
    if request.method == 'POST':
        buy_book = request.form.get('buy_book')
        bought_book = Books.query.filter_by(book_name=buy_book).first()
        if bought_book:
            bought_book.owner = current_user.id
            db.session.commit()
    books = Books.query.all()
    return render_template('index.html.j2', books=books, buy=buy)

@app.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out', 'danger')
        return redirect(url_for('login'))

@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    try:
        book_id = request.form.get('book_id')
        book = Books.query.filter_by(id=book_id).first()
        if request.method == 'POST' and book_id:
            DictBooks = {
                book_id: {'name': book.book_name,
                        'price': book.price}
            }
            if 'Cart' in session:
                print(session['Cart'])
                if book_id in session['Cart']:
                    print("This product is already in your cart")
                else:
                    session['Cart'] = mergeDicts(session['Cart'], DictBooks)
                    return redirect(request.referrer)
            else:
                session['Cart'] = DictBooks
                return redirect(request.referrer)


    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('index'))
    except Exception as e:
        print(e)

@app.route('/cart')
@login_required
def cart():
    if 'Cart' not in session:
        return redirect(request.referrer)
    total = 0
    for key, book in session['Cart'].items():
        total += book['price']
    tax = total * 0.0825
    tax = float(tax)
    total = total * 1.0825
    return render_template('cart.html.j2', total=total, tax=tax)

@app.route('/delete/<int:id>')
def delete(id):
    if 'Cart' not in session and len(session['Cart']) <= 0:
        return redirect(url_for('index'))
    try:
        session.modified = True
        for key, book in session['Cart'].items():
            if int(key) == id:
                session['Cart'].pop(key, None)
                return redirect(url_for('cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('cart'))



##################
###### LOGIN STUFF
##################
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get("email").lower()
        password = request.form.get("password")
        u = User.query.filter_by(email=email).first()

        if u and u.check_hashed_password(password):
            login_user(u)
            flash('You have logged in', 'success')
            return redirect(url_for("index"))
        error_string = "Invalid Email password combo"
        return render_template('login.html.j2', error = error_string, form=form)
    return render_template('login.html.j2', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password": form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
        except:
            error_string = "There was an unexpected Error creating your account. Please Try again."
            return render_template('register.html.j2',form=form, error = error_string)
        return redirect(url_for('login'))
    return render_template('register.html.j2', form = form)