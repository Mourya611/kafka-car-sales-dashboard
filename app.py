from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend (JS) to access backend

# In-memory storage of all car orders
car_sales = []

@app.route('/')
def home():
    return "🚀 Car Sales Backend is running!"

@app.route('/new_car', methods=['POST'])
def new_car():
    try:
        data = request.get_json()
        if data:
            car_sales.append(data)
            return jsonify({"message": "✅ Order received"}), 200
        else:
            return jsonify({"error": "No data received"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/all_cars', methods=['GET'])
def all_cars():
    return jsonify(car_sales)

if __name__ == '__main__':
    app.run(debug=True)
