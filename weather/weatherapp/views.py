from datetime import datetime
from django.shortcuts import render
import requests

def home(request):
    city = ''
    temp = ''
    description = ''
    icon = ''
    day = ''

    if request.method == 'POST':
        city = request.POST.get('city')
        # Example API call (replace with your actual logic)
        # Example: Using OpenWeatherMap API
        API_KEY = 'ffc5d1d87dc9e9cdbcaa94559a9949b1'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()

        if data['cod'] == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            day = datetime.fromtimestamp(data['dt'])

    return render(request, 'index.html', {
        'city': city,
        'temp': temp,
        'description': description,
        'icon': icon,
        'day': day,
    })