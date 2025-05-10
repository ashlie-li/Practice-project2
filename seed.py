from models import db, User, Customers, Orders
from flask import Flask
import datetime

if __name__ == "__main__":
    app = Flask(__name__)
    # Update with your database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/sample_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        # Drop and recreate tables
        db.drop_all()
        db.create_all()

        # Add dummy data to the User table
        users = [
            User(username="admin_user", password="admin123", role_type="admin"),
            User(username="manager_user",
                 password="manager123", role_type="manager"),
            User(username="customer_user",
                 password="customer123", role_type="customer"),
        ]

        # Add dummy data to the Customers table
        customers = [
            Customers(customer_name="John Doe", signup_date=datetime.date(
                2022, 1, 15), region="North"),
            Customers(customer_name="Jane Smith",
                      signup_date=datetime.date(2022, 3, 10), region="South"),
            Customers(customer_name="Alice Johnson",
                      signup_date=datetime.date(2022, 5, 20), region="East"),
        ]

        # Add dummy data to the Orders table
        orders = [
            Orders(customer_id=1, order_date=datetime.date(2023, 1, 10), product_category="Electronics",
                   order_amount=250.75, payment_method="Credit Card"),
            Orders(customer_id=2, order_date=datetime.date(2023, 2, 5), product_category="Books",
                   order_amount=45.50, payment_method="PayPal"),
            Orders(customer_id=3, order_date=datetime.date(2023, 3, 15), product_category="Clothing",
                   order_amount=89.99, payment_method="Debit Card"),
        ]

        # Insert data into the database
        db.session.bulk_save_objects(users)
        db.session.bulk_save_objects(customers)
        db.session.bulk_save_objects(orders)
        db.session.commit()

        print("Dummy data inserted into the User, Customers, and Orders tables.")
