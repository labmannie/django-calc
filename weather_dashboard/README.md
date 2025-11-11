# Weather Dashboard

This is a simple Django app to display the weather of a city.

## Setup

1.  **Install the required packages**:
    ```
    pip install django-bootstrap4 requests python-dotenv
    ```
2.  **Create a `.env` file** in the `myproject` directory with the following content, replacing `YOUR_API_KEY` and `YOUR_GEMINI_API_KEY` with your actual keys:
    ```
    WEATHER_API_KEY=YOUR_API_KEY
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY
    ```
3.  **Add the app to `INSTALLED_APPS`** in `myproject/settings.py`:
    ```python
    INSTALLED_APPS = [
        ...
        'weather_dashboard',
        'bootstrap4',
    ]
    ```
4.  **Include the app's URLs** in `myproject/urls.py`:
    ```python
    urlpatterns = [
        ...
        path('weather/', include('weather_dashboard.urls')),
    ]
    ```
5.  **Run the migrations**:
    ```
    python manage.py makemigrations weather_dashboard
    python manage.py migrate
    ```
6.  **Run the development server**:
    ```
    python manage.py runserver
    ```
7.  **Access the weather dashboard** at `http://127.0.0.1:8000/weather/`.
