# Django Calculator

A simple web-based calculator application built with Django.

## Description

This project is a simple calculator that can perform basic arithmetic operations. It's a demonstration of a simple Django application. The project also includes a "Hello World" page.

This project was created by **Lab Man NIE**, a lab worker at NIE.

## Features

*   Basic arithmetic operations: addition, subtraction, multiplication, division.
*   A simple and clean user interface.
*   A "Hello World" page at the root URL.

## Getting Started

### Prerequisites

*   Python 3.x
*   Django

### Installation

1.  **Clone the repository.**
2.  **Navigate to the project directory:**
    ```bash
    cd myproject
    ```
3.  **Create and activate a virtual environment:**
    ```bash
    # On Windows
    python -m venv ..\testenv
    ..\testenv\Scripts\activate

    # On macOS/Linux
    python3 -m venv ../testenv
    source ../testenv/bin/activate
    ```
4.  **Install Django:**
    ```bash
    pip install Django
    ```
5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
6.  **Open your browser and navigate to the following URLs:**
    *   **Hello World:** `http://127.0.0.1:8000/`
    *   **Calculator:** `http://127.0.0.1:8000/calculator/`

## Usage

*   The main page will display a "Hello World" message from Shreyas.
*   Navigate to `/calculator` to use the calculator.

## Weather dashboard — API key

The project includes a simple weather dashboard (`/weather/` or the URL configured in the project).

The dashboard requires an OpenWeatherMap API key. Set the key in one of these ways. The app accepts several common variable names; use any of:

```
WEATHER_API_KEY=your_openweathermap_api_key_here
OPENWEATHER_API_KEY=your_openweathermap_api_key_here
OPEN_WEATHER_API_KEY=your_openweathermap_api_key_here
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here
```

1. Create a `.env` file at the project root (same directory as `manage.py`) with one of the lines above (no quotes).

2. Or set the environment variable in your OS. On Windows PowerShell you can run:

```powershell
$env:WEATHER_API_KEY = "your_openweathermap_api_key_here"
```

After adding the key, restart the Django development server. The settings file already reads `.env` using `python-dotenv`.

To obtain an API key, sign up at https://openweathermap.org/ and get a Free API key.

## Author

*   **Lab Man NIE**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
