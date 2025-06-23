# 🚗 Real-Time Car Sales Dashboard using Kafka, Flask & HTML

This project demonstrates a **real-time full-stack dashboard** built with:
- **Kafka** for streaming car sale data
- **Python (Producer & Consumer)**
- **Flask** as the backend API
- **HTML + JavaScript** as the frontend dashboard

---

## 📌 Project Overview

A CSV dataset of car sales is streamed using a Kafka Producer. A Kafka Consumer listens for incoming data and pushes it to a Flask API. The frontend dashboard auto-refreshes and displays new car sale records in real-time.

---

## 📂 Folder Structure

car-sales-project/
├── producer.py # Kafka producer script (sends car data)
├── consumer_to_flask.py # Kafka consumer that pushes data to Flask
├── app.py # Flask backend server
├── frontend/
│ └── index.html # Client-side live dashboard

---

## ⚙️ Tech Stack

| Layer        | Technology                         |
|--------------|-------------------------------------|
| Producer     | Python + Pandas + Confluent Kafka   |
| Messaging    | Apache Kafka (Confluent Cloud)      |
| Consumer     | Python Kafka Client                 |
| Backend API  | Flask + Flask-CORS                  |
| Frontend     | HTML + JavaScript (AJAX)            |

---

## ▶️ How It Works

1. **Kafka Producer** reads car sales data from CSV and sends it to Kafka topic.
2. **Kafka Consumer** listens for messages and sends each record to the Flask API.
3. **Flask Server** stores the data in-memory and provides it via a REST endpoint.
4. **Frontend Dashboard** polls the Flask API every 2 seconds and shows live data with a popup alert.

---

## 🚀 Running the Project

### Step 1: Install Dependencies

```bash
pip install flask flask-cors confluent_kafka pandas

Step 2: Start Flask Backend

python app.py
Runs on: http://localhost:5000

Step 3: Start Kafka Consumer

python consumer_to_flask.py
This will listen for incoming Kafka messages and POST them to Flask.

Step 4: Open the Frontend
Go to the frontend/ folder

Open index.html in your browser (Chrome/Edge)

You’ll see a live-updating table and popup: ✅ "Your order is taken"


Step 5: Start Kafka Producer

python producer.py
Streams car sale records from CSV to Kafka topic.

📊 Sample Output
Frontend shows:

Car Name	Brand	Model	Price
Maruti Alto	Maruti	800	₹2,50,000
Hyundai i20	Hyundai	Sportz	₹5,60,000

✅ Popups appear for each new order received.