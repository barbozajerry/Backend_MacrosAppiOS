from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# PostgreSQL connection setup
conn = psycopg2.connect(
    host="localhost",
    port=5434,
    database="Macros_app",
    user="postgres",
    password="123abc"
)
cursor = conn.cursor()

@app.route("/", methods=["GET"])
def home():
    return "✅ Flask server is running!"

@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "User already exists"}), 409

        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/data", methods=["POST"])
def submit_data():
    data = request.get_json()
    user_id = 1

    cursor.execute("""
        INSERT INTO health_data (user_id, carbs, protein, fats, steps, current_weight, weight_goal)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        data.get("carbs"),
        data.get("protein"),
        data.get("fats"),
        data.get("steps"),
        data.get("current_weight"),
        data.get("weight_goal")
    ))
    conn.commit()

    return jsonify({"message": "Health data submitted"}), 201

if __name__ == "__main__":
    app.run(debug=True)
