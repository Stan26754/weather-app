from flask import Flask, jsonify, request, send_from_directory
import requests
import os
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv("weather.env")
API_KEY = os.getenv("API_KEY")
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/")
def home():
    return send_from_directory(".", "weather.html")
@app.route("/script.js")
def script():
    return send_from_directory(".", "script.js")
@app.route("/style.css")
def style():
    return send_from_directory(".", "style.css")

@app.route("/weather")
def weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "Please enter a city name."}), 400

    try:
        response = requests.get(
            OPENWEATHER_URL,
            params={
                "q": city,
                "appid": API_KEY,
                "units": "metric",
            },
            timeout=10,
        )

        if not response.ok:
            try:
                error_data = response.json()
                message = error_data.get("message", "Weather service request failed.")
            except ValueError:
                message = "Weather service request failed."

            return jsonify({"error": message}), response.status_code

        return jsonify(response.json())

    except requests.RequestException:
        return jsonify({
            "error": "Could not connect to the weather service."
        }), 502


if __name__ == "__main__":
    app.run(debug=True)
    