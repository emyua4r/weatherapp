
from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# WeatherAPI.com API Key (provided by the user)
API_KEY = '51d6b1325ac14eb680543912241310'

# Function to get weather data by city name
def get_weather(city):
    url = f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=10&aqi=yes&alerts=yes'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {'message': 'City not found. Please ensure the city name is valid.'}

# Function to get location by IP (for automatic detection)
def get_location(ip):
    location_url = f"http://ip-api.com/json/"
    response = requests.get(location_url)
    if response.status_code == 200:
        return response.json()
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    location_data = None
    ip = request.remote_addr  # Get the IP of the user
    if request.method == 'POST':
        city = request.form['city'].strip()
        weather_data = get_weather(city)
    else:
        location_data = get_location(ip)
        if location_data and location_data['status'] == 'success':
            city = location_data['city']
            weather_data = get_weather(city)
    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
