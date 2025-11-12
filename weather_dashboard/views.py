from django.shortcuts import render
import requests
import os
import logging
from .forms import CityForm
from django.conf import settings
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def _to_local_time(ts, tz_offset_seconds):
    try:
        return datetime.utcfromtimestamp(ts + tz_offset_seconds).strftime('%Y-%m-%d %H:%M')
    except Exception:
        return None


def get_weather(city):
    """Fetch current weather and return structured data or {'error': msg}.

    Adds extra fields used by the enhanced UI: humidity, feels_like, pressure,
    wind speed/direction, sunrise/sunset (local), coordinates, country, updated_at.
    """
    api_key = getattr(settings, 'WEATHER_API_KEY', None) or os.getenv('WEATHER_API_KEY')
    if not api_key:
        logger.warning('OpenWeather API key is not configured')
        return {'error': 'Weather API key not configured. Set WEATHER_API_KEY in .env or environment.'}

    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}

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
        try:
            msg = resp.json().get('message')
            return {'error': f'Weather service error {resp.status_code}: {msg}'}
        except Exception:
            return {'error': f'Weather service returned status {resp.status_code}.'}

    try:
        data = resp.json()
        main = data.get('main', {})
        weather = (data.get('weather') or [{}])[0]
        wind = data.get('wind', {})
        sys = data.get('sys', {})
        tz = data.get('timezone', 0)

        weather_data = {
            'city': data.get('name'),
            'country': sys.get('country'),
            'temperature': main.get('temp'),
            # condition: short label like 'Clear', 'Clouds', 'Rain'
            'condition': (weather.get('main') or '').lower(),
            'feels_like': main.get('feels_like'),
            'humidity': main.get('humidity'),
            'pressure': main.get('pressure'),
            'description': weather.get('description'),
            'icon': weather.get('icon'),
            'wind_speed': wind.get('speed'),
            'wind_deg': wind.get('deg'),
            'sunrise': _to_local_time(sys.get('sunrise') or 0, tz),
            'sunset': _to_local_time(sys.get('sunset') or 0, tz),
            'coords': data.get('coord'),
            'updated_at': _to_local_time(data.get('dt') or 0, tz),
        }

        # icon url
        if weather_data.get('icon'):
            weather_data['icon_url'] = f"https://openweathermap.org/img/wn/{weather_data['icon']}@2x.png"

        return {'data': weather_data}
    except Exception:
        logger.exception('Failed to parse JSON from OpenWeather API')
        return {'error': 'Invalid response from weather service.'}


def weather_dashboard(request):
    """Enhanced dashboard view with recent searches stored in session."""
    error = None
    weather_data = None

    # recent searches (store last 5)
    recent = request.session.get('recent_searches', [])

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
                # update recent searches
                if weather_data and weather_data.get('city'):
                    city_name = f"{weather_data.get('city')}, {weather_data.get('country') or ''}".strip().strip(',')
                    if city_name in recent:
                        recent.remove(city_name)
                    recent.insert(0, city_name)
                    recent = recent[:5]
                    request.session['recent_searches'] = recent
    else:
        form = CityForm()

    return render(request, 'weather_dashboard/weather_dashboard.html', {
        'form': form,
        'weather_data': weather_data,
        'error': error,
        'recent': recent,
    })

