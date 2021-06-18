import os
import requests

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
from geopy.geocoders import Nominatim


################################################################################
# SETUP
################################################################################

app = Flask(__name__)

load_dotenv()

pp = PrettyPrinter(indent=4)

API_KEY = os.getenv('API_KEY')
API_URL = 'http://api.openweathermap.org/data/2.5/weather'


################################################################################
# ROUTES
################################################################################

@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""
    context = {
        'min_date': (datetime.now() - timedelta(days=5)),
        'max_date': datetime.now()
    }
    return render_template('home.html', **context)

# def get_letter_for_units(units):
#     """Returns a shorthand letter for the given units."""
#     return 'F' if units == 'imperial' else 'C' if units == 'metric' else 'K'


@app.route('/results')
def results():
    mood = request.args.get('mood')
    city = request.args.get('city')
    # units = request.args.get('units')

    params = {
        'appid': API_KEY,
        'q': city,
        # 'units': units
    }
    result_json = requests.get(API_URL, params=params).json()
    pp.pprint(result_json)

    context = {
        'mood' : mood,
        'date': datetime.now(),
        'city': city,
        'description': result_json['weather'][0]['description'],
        'temp': result_json['main']['temp'],
        # 'units_letter': get_letter_for_units(units)
    }

    return render_template('results.html', **context)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
