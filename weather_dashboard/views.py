from django.shortcuts import render
import requests
import os
import logging
from .forms import CityForm
from django.conf import settings

logger = logging.getLogger(__name__)


def get_weather(city):
    """Return weather data dict or dict containing 'error'.

    Reads API key from Django settings (WEATHER_API_KEY) or environment.
    Handles network and API errors and returns a helpful error message.
    """
    api_key = getattr(settings, 'WEATHER_API_KEY', None) or os.getenv('WEATHER_API_KEY')
    if not api_key:
        logger.warning('OpenWeather API key is not configured')
        return {'error': 'Weather API key not configured. Set WEATHER_API_KEY in .env or environment.'}

    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',  # For Celsius
    }

    try:
        resp = requests.get(base_url, params=params, timeout=10)
    except requests.RequestException as exc:
        logger.exception('Network error when calling OpenWeather API')
        return {'error': f'Network error when contacting weather service: {exc}'}

    if resp.status_code == 401:
        logger.warning('Unauthorized from weather API (likely invalid API key): %s', resp.text)
        return {'error': 'Unauthorized: invalid or missing weather API key.'}

    if resp.status_code != 200:
        logger.error('OpenWeather API returned %s: %s', resp.status_code, resp.text)
        return {'error': f'Weather service returned status {resp.status_code}.'}

    try:
        data = resp.json()
        weather_data = {
            'city': data.get('name'),
            'temperature': data.get('main', {}).get('temp'),
            'description': data.get('weather', [{}])[0].get('description'),
            'icon': data.get('weather', [{}])[0].get('icon'),
        }
        return {'data': weather_data}
    except ValueError:
        logger.exception('Failed to parse JSON from OpenWeather API')
        return {'error': 'Invalid response from weather service.'}


def weather_dashboard(request):
    """View for weather dashboard. Returns form, weather data (if any), and error message (if any)."""
    error = None
    weather_data = None

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            result = get_weather(city)
            if result is None:
                error = 'Unexpected error getting weather.'
            elif 'error' in result:
                error = result['error']
            else:
                weather_data = result.get('data')
    else:
        form = CityForm()

    return render(request, 'weather_dashboard/weather_dashboard.html', {
        'form': form,
        'weather_data': weather_data,
        'error': error,
    })

