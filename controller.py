from flask import Flask, jsonify, request, abort
from models import db, Orders, Customers, User
from token_generator import TokenGenerator

app = Flask(__name__)

# PostgreSQL database URI format:
# postgresql://username:password@host:port/dbname
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/sample_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Example token for simplicity
AUTHORIZED_TOKEN = "your_secure_token"


def require_valid_token(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            abort(401, description="Unauthorized: Missing or invalid token")

        token = token.split("Bearer ")[1]  # Extract the token part
        try:
            decoded = TokenGenerator.decode_token(token)
            request.user_id = decoded["user_id"]
            request.role_type = decoded["role_type"]
        except ValueError as e:
            abort(401, description=str(e))

        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # Preserve function name for Flask
    return wrapper


@app.route("/orders", methods=["GET"])
@require_valid_token
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


@app.route("/orders", methods=["POST"])
@require_valid_token
def add_order():
    data = request.json
    try:
        new_order = Orders(
            customer_id=data["customer_id"],
            order_date=data["order_date"],
            product_category=data["product_category"],
            order_amount=data["order_amount"],
            payment_method=data["payment_method"]
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({"message": "Order added successfully"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/customers", methods=["GET"])
@require_valid_token
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


@app.route("/customers", methods=["POST"])
@require_valid_token
def add_customer():
    data = request.json
    try:
        new_customer = Customers(
            customer_name=data["customer_name"],
            signup_date=data["signup_date"],
            region=data.get("region")  # Optional field
        )
        db.session.add(new_customer)
        db.session.commit()
        # return the object as a response
        return jsonify({
            "customer_id": new_customer.id,
            "name": new_customer.customer_name,
            "signup_date": new_customer.signup_date.isoformat(),
            "region": new_customer.region
        }), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    try:
        username = data["username"]
        password = data["password"]

        # Validate user credentials
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Replace with hashed password check if applicable
            token = TokenGenerator.generate_token(user.id, user.role_type)
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
