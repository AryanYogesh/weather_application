from flask import Flask, render_template,request,jsonify
import requests

app = Flask(__name__, static_folder='static')

API_KEY = "703cba0db67d8e55633646fbf47f5ede"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather", methods=["POST"]) 
def get_weather():
    city = request.form.get("city")
    if not city:
        return jsonify({"error":"city name is required"}),400
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city":data["name"],
            "country":data["sys"]["country"],
            "temperature":data["main"]["temp"],
            "description":data["weather"][0]["description"]
        }
        return jsonify(weather_info)
    else:
        return jsonify({"error":"city not found please enter a valid city"}),404
    

# Add this new route to your existing Flask application code
@app.route("/forecast", methods=["POST"])
def get_forecast():
    city = request.form.get("city")
    if not city:
        return jsonify({"error": "City name is required"}), 400

    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(forecast_url)

    if response.status_code == 200:
        data = response.json()
        forecast_data = []

        # Extract relevant data for each 3-hour interval
        for forecast in data["list"]:
            forecast_info = {
                "date": forecast["dt_txt"],  # Date and time
                "temperature": forecast["main"]["temp"],  # Temperature in Celsius
                "description": forecast["weather"][0]["description"],  # Weather condition
                "icon": forecast["weather"][0]["icon"]  # Weather icon code
            }
            forecast_data.append(forecast_info)

        return jsonify({"city": data["city"]["name"], "country": data["city"]["country"], "forecast": forecast_data})
    else:
        return jsonify({"error": "City not found, please enter a valid city"}), 404

    
if __name__=="__main__":
    app.run(debug=True)