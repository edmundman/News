
import requests

api_key = "7edd7f6c7c02a7cdebb4dbb1dc0b0d9e"  # Replace with your actual API key

def get_weather(api_key, city="Bristol,UK"):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # You can change this to "imperial" for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            weather_info = f"Weather in {city}: {weather_description.capitalize()}\n"
            weather_info += f"Temperature: {temperature}°C\n"
            weather_info += f"Humidity: {humidity}%\n"
            weather_info += f"Wind Speed: {wind_speed} m/s"

            return weather_info
        else:
            return f"Failed to fetch weather data. Error code: {response.status_code}"

    except Exception as e:
        return f"An error occurred: {str(e)}"