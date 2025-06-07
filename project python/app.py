from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float)
    description = db.Column(db.String(200))
    image = db.Column(db.String(200))

# Routes
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        subtotal = product.price * quantity
        total += subtotal
        items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return render_template('cart.html', items=items, total=total)

@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return "Thank you for your purchase!"

# Run this once to create the DB and some products
@app.cli.command('create_db')
def create_db():
    db.create_all()
    db.session.add_all([
        Product(name='T-Shirt', price=19.99, description='Nice cotton t-shirt.', image='https://via.placeholder.com/150'),
        Product(name='Sneakers', price=49.99, description='Comfortable running shoes.', image='https://via.placeholder.com/150'),
        Product(name='Hat', price=14.99, description='Stylish hat.', image='https://via.placeholder.com/150'),
    ])
    db.session.commit()
    print("Database initialized with sample products.")

if __name__ == '__main__':
    app.run(debug=True)
