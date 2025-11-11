import os
from pathlib import Path
import requests

# try to load .env
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / '.env')
except Exception:
    pass

names = ['WEATHER_API_KEY', 'OPENWEATHER_API_KEY', 'OPEN_WEATHER_API_KEY', 'OPENWEATHERMAP_API_KEY']
key = None
found_name = None
for n in names:
    v = os.getenv(n)
    if v:
        key = v
        found_name = n
        break

if not key:
    print('ERROR: WEATHER API key not found in environment or .env (checked names:', ','.join(names) + ')')
    raise SystemExit(1)

print(f'Using {found_name}: present (length={len(key)})')

url = 'https://api.openweathermap.org/data/2.5/weather'
params = {'q': 'London', 'appid': key}

try:
    r = requests.get(url, params=params, timeout=10)
    print('HTTP', r.status_code)
    try:
        j = r.json()
        print('Response JSON:', j)
        if r.status_code == 401:
            print('\nHint: 401 means OpenWeather rejected the key. Common fixes:')
            print(' - Wait a few minutes after creating a new key')
            print(' - Ensure you copied the "API key" for Current Weather Data')
            print(' - Regenerate the key in your OpenWeather dashboard')
    except Exception:
        print('Response text:', r.text[:1000])
except Exception as e:
    print('Network error:', e)
    raise
