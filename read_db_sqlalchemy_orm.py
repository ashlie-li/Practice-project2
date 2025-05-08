from flask import Flask, jsonify, request, abort
from models import db, Orders, Customers

app = Flask(__name__)

# PostgreSQL database URI format:
# postgresql://username:password@host:port/dbname
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/sample_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Example token for simplicity
AUTHORIZED_TOKEN = "your_secure_token"


def require_authorization(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token != f"Bearer {AUTHORIZED_TOKEN}":
            abort(401, description="Unauthorized")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # Preserve function name for Flask
    return wrapper


@app.route("/orders", methods=["GET"])
def show_orders():
    rows = Orders.query.all()
    json_ready_data = [
        {
            "transaction_id": row.id,
            "user_id": row.customer_id,
            "date": row.order_date.isoformat(),
            "category": row.product_category,
            "amount": row.order_amount,
            "payment_method": row.payment_method
        }
        for row in rows
    ]
    return jsonify(json_ready_data)


@app.route("/customers", methods=["GET"])
@require_authorization
def show_customers():
    rows = Customers.query.all()
    json_ready_data = [
        {
            "customer_id": row.id,
            "name": row.customer_name,
            "signup_date": row.signup_date,
            "region": row.region
        }
        for row in rows
    ]
    return jsonify(json_ready_data)


if __name__ == '__main__':
    app.run(debug=True)
