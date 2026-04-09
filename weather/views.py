import requests
from datetime import datetime, timedelta
from django.shortcuts import render


def index(request):
    weather_data = {}
    if request.method == "POST":
        city = request.POST["city"]
        option = request.POST.get(
            "option", "current"
        )  # Get the selected option as default
        api_key = "80d36a642bf4b686eba6a70a6350e53f"
        # This should ideally be in environment variables for security, but hardcoded here for simplicity

        # Get city coordinates for historical or forecast data
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)
        if geo_response.status_code == 200 and geo_response.json():
            geo_data = geo_response.json()[0]
            lat, lon = geo_data["lat"], geo_data["lon"]
        else:
            weather_data["error"] = "City not found. Try entering another city!"
            return render(request, "weather/index.html", {"weather_data": weather_data})

        if option == "current":
            # Current weather right now
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data["wind"]["speed"],
                    "wind_direction": data["wind"]["deg"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                }
            else:
                weather_data["error"] = "City not found. Try entering another city!"

        elif option == "forecast":
            # Upcoming weather forecast for a short time range (next 8 forecasts, typically 3-hour intervals)
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                forecast_list = []
                for forecast in data["list"][:8]:  # Get the next 8 forecasts
                    forecast_list.append(
                        {
                            "datetime": forecast["dt_txt"],
                            "temperature": forecast["main"]["temp"],
                            "description": forecast["weather"][0]["description"],
                            "humidity": forecast["main"]["humidity"],
                            "pressure": forecast["main"]["pressure"],
                            "wind_speed": forecast["wind"]["speed"],
                            "wind_direction": forecast["wind"]["deg"],
                            "icon": forecast["weather"][0]["icon"],
                        }
                    )
                weather_data = {
                    "city": data["city"]["name"],
                    "forecast": forecast_list,
                }
            else:
                weather_data["error"] = "Unable to fetch forecast data."

    # Always pass an `errors` mapping to the template (template expects `errors.city` possibility)
    return render(
        request, "weather/index.html", {"weather_data": weather_data, "errors": {}}
    )
