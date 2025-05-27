import re
import requests
from urllib.parse import urlparse
from django.contrib import messages  # Correct import for Django messages
from datetime import datetime
from django.shortcuts import render

def is_valid_image_url(url):
    """Check if the URL is a valid image URL (ends with .jpg, .png, etc.)."""
    if not url:
        return False
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return False
    return any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif'])

def home(request):
    city = ''
    temp = ''
    description = ''
    icon = ''
    day = ''
    image_url = 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1920&h=1080&dpr=1'  # Valid default image

    if request.method == 'POST':
        city = request.POST.get('city')
        API_KEY = 'ffc5d1d87dc9e9cdbcaa94559a9949b1'
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        try:
            if weather_data['cod'] == 200:
                temp = weather_data['main']['temp']
                description = weather_data['weather'][0]['description']
                icon = weather_data['weather'][0]['icon']
                day = datetime.fromtimestamp(weather_data['dt'])

                # Image search API call
                ENGINE_KEY = 'AIzaSyBmSQV4nuSgOQuNCLYC2YOjAP8ZaMU8gak'
                SEARCH_ENGINE_ID = '8791704d43cf245cb'
                query = f"{city} 1920x1080"
                image_search_url = (
                    f'https://www.googleapis.com/customsearch/v1?key={ENGINE_KEY}'
                    f'&cx={SEARCH_ENGINE_ID}&q={query}&start=1&searchType=image&imgSize=xlarge'
                )
                image_response = requests.get(image_search_url)
                image_data = image_response.json()
                search_items = image_data.get("items", [])

                # Safely get the first image link or use the default
                if search_items:
                    candidate_url = search_items[0].get('link', '')
                    if is_valid_image_url(candidate_url):
                        image_url = candidate_url
                    else:
                        image_url = 'https://via.placeholder.com/1920x1080'  # Fallback if invalid
                else:
                    image_url = 'https://via.placeholder.com/1920x1080'  # Fallback if no results

                return render(request, 'index.html', {
                    'city': city,
                    'temp': temp,
                    'description': description,
                    'icon': icon,
                    'day': day,
                    'exception_occured': False,
                    'image_url': image_url
                })
            else:
                messages.error(request, 'Failed to fetch weather data for the city.')
                return render(request, 'index.html', {
                    'city': 'Sri Lanka',
                    'temp': 25,
                    'description': 'clear sky',
                    'icon': '01d',
                    'day': datetime.date.today(),
                    'exception_occured': True,
                    'image_url': image_url  # Default image
                })
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return render(request, 'index.html', {
                'city': 'Sri Lanka',
                'temp': 25,
                'description': 'clear sky',
                'icon': '01d',
                'day': datetime.date.today(),
                'exception_occured': True,
                'image_url': image_url  # Default image
            })

    # Default GET request rendering
    return render(request, 'index.html', {
        'city': '',
        'temp': '',
        'description': '',
        'icon': '',
        'day': '',
        'exception_occured': False,
        'image_url': image_url  # Default image
    })