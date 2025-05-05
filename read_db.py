import os
from flask import Flask, Blueprint, jsonify, request, render_template
import psycopg2
from psycopg2.extras import RealDictCursor


class Config:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@127.0.0.1:5432/sample_db"
    )


def get_db_connection():
    return psycopg2.connect(
        Config.DATABASE_URL,
        cursor_factory=RealDictCursor
    )


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/customers", methods=["GET"])
def show_customers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers;")
    customers = cur.fetchall()
    cur.close()
    conn.close()
    # Render HTML table

    # return render_template("table.html", rows=customers, columns=["id", "name", "signup_date", "region"])
    return jsonify(customers)
