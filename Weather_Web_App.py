from flask import Flask, render_template, request
import geocoder
import requests

app = Flask(__name__)

WEATHER_API_URL = "https://api.weather.gov/points/{},{}/forecast"

def get_location(latitude, longitude):
    try:
        location = geocoder.osm([latitude, longitude], method='reverse')
        return location.address if location else "Location not found"
    except Exception as e:
        return str(e)

def get_weather_info(latitude, longitude):
    try:
        # Get forecast URL
        response = requests.get(f"https://api.weather.gov/points/{latitude},{longitude}")
        response_data = response.json()
        forecast_url = response_data['properties']['forecast']

        # Get actual forecast data
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()
        # Extracting the first forecast from the list as an example
        forecast = forecast_data['properties']['periods'][0]
        temperature = forecast['temperature']
        wind_speed = forecast['windSpeed']
        short_forecast = forecast['shortForecast']

        return {
            "temperature": temperature,
            "wind_speed": wind_speed,
            "short_forecast": short_forecast
        }
    except:
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    weather_info = {}
    location_name = "Enter a Pair of Coordinates"
    if request.method == "POST":
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        weather_info = get_weather_info(latitude, longitude)
        location_name = get_location(latitude, longitude)
    return render_template("index.html", weather=weather_info, location_name=location_name)

if __name__ == "__main__":
    app.run(debug=True)
