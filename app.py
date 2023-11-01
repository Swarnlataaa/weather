from flask import Flask, request, jsonify
import requests

app = Flask(__name)

# Replace with your own Google Maps API key and OpenWeatherMap API key
GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'
OPENWEATHERMAP_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'

@app.route('/weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')
    
    # Use Google Geocoding API to get latitude and longitude from the location name
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_MAPS_API_KEY}'
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()

    if geocoding_data.get('status') == 'OK':
        lat = geocoding_data['results'][0]['geometry']['location']['lat']
        lng = geocoding_data['results'][0]['geometry']['location']['lng']
        
        # Use OpenWeatherMap API to get weather data based on the coordinates
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Location not found'})

if __name__ == '__main__':
    app.run(debug=True)
