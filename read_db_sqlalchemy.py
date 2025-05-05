from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import psycopg2
from psycopg2.extras import RealDictCursor


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

# PostgreSQL database URI format:
# postgresql://username:password@host:port/dbname
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/sample_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Reflect the existing table


@app.route("/orders", methods=["GET"])
def show_orders():
    Orders = db.Table('orders', db.metadata, autoload_with=db.engine)
    rows = db.session.query(Orders).all()
    breakpoint()
    # json_ready_data = [
    #     {
    #         "transaction_id": t[0],
    #         "user_id": t[1],
    #         "date": t[2].isoformat(),
    #         "category": t[3],
    #         "amount": float(t[4]),
    #         "payment_method": t[5]
    #     }
    #     for t in rows
    # ]
    # Convert each row to a dict
    # orders = [row for row in rows]
    return jsonify([list(row) for row in rows])
    # return "hello world"


if __name__ == '__main__':
    app.run(debug=True)
