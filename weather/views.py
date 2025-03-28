import requests
from django.shortcuts import render

def index(request):
    weather_data = {}
    if request.method == 'POST':
        city = request.POST['city']
        api_key = 'SECRET_KEY'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'

        response = requests.get(url)
        if response.status_code == 200: # If the city is found 
            data = response.json()
            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind']['deg'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
        else: # If the city is not found
            weather_data['error'] = 'City not found. Try entering another city!'

    return render(request, 'weather/index.html', {'weather_data': weather_data})
