import os
from pathlib import Path

# Try to load .env so this script works standalone
try:
    from dotenv import load_dotenv
    base_dir = Path(__file__).resolve().parent.parent
    env_path = base_dir / '.env'
    load_dotenv(env_path)
except Exception:
    env_path = None

names = ['WEATHER_API_KEY', 'OPENWEATHER_API_KEY', 'OPEN_WEATHER_API_KEY', 'OPENWEATHERMAP_API_KEY']
found_name = None
found_key = None
for n in names:
    v = os.getenv(n)
    if v:
        found_name = n
        found_key = v
        break

if env_path:
    print(f'Tried to load .env from: {env_path}')
else:
    print('python-dotenv not available; did not attempt to load .env')

if not found_key:
    print('WEATHER_API_KEY: NOT SET (no env var found)')
else:
    print(f'Using environment variable: {found_name} (length={len(found_key)})')
    masked = '*' * max(0, len(found_key) - 4) + found_key[-4:]
    print('Masked key preview:', masked)
