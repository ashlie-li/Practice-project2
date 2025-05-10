from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    product_category = db.Column(db.String, nullable=False)
    order_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String, nullable=False)


class Customers(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String, nullable=False)
    signup_date = db.Column(db.Date, nullable=False)
    region = db.Column(db.String, nullable=True)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role_type = db.Column(db.String(20), nullable=False)

    def __init__(self, username, password, role_type):
        self.username = username
        self.password = password
        self.role_type = role_type
