import random
import requests
import json

# цільові URL у списку
target_urls = ['https://www.google.com', 'https://www.facebook.com', 'https://www.twitter.com', 'https://www.amazon.com', 'https://www.apple.com']
# обираємо рандомний URL зі списку
random_url = random.choice(target_urls)
# поміщаємо запит до рандомного URL зі списку у змінну
res = requests.get(random_url)
# виводимо необхідні нам дані: статус-код, URL, довжину відповіді на запит до URL
print(f'Status code: {res.status_code}')
print(f'URL: {random_url}')
print(f'Length of response: {len(res.text)}')
# відділяємо одне завдання від іншого
print("="*10)
# поле вводу назви міста користувачем
city = input("Введіть назву міста латиницею: ")
# URL для пошуку міста по назві на open-meteo
geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
# запит на пошук міста
geocode_response = requests.get(geocode_url)
# відповідь open-meteo на наш запит
geocode_data = geocode_response.json()
# Додаємо обробку помилок на випадок якщо місто не знайдене
try:
    # витягаємо кординати міста з відповіді open-meteo на наш запит
    latitude = geocode_data['results'][0]['latitude']
    longitude = geocode_data['results'][0]['longitude']
    # URL для пошуку погоди по координатам міста
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&windspeed_unit=ms&timezone=Europe/Kiev"
    # запит на пошук погоди по координатам міста
    weather_response = requests.get(weather_url)
    # відповідь на наш запит
    weather_data = weather_response.json()
    # з відповіді беремо необхідну нам частину з погодою
    current_weather = weather_data['current_weather']
    # перелік приблизних розшифровок статусу погоди з open-meteo
    weather_code = {
        0: 'Безхмарно',
        1: 'Переважно безхмарно',
        2: 'Хмарно з проясненнями',
        3: 'Похмуро', 45: 'Туман',
        48: 'Іней',
        51: 'Слабка мряка',
        53: 'Помірна мряка',
        55: 'Густа мряка',
        56: 'Легкий крижаний дощ',
        57: 'Щільний крижаний дощ',
        61: 'Слабкий дощ',
        63: 'Помірний дощ',
        65: 'Сильний дощ',
        66: 'Слабкий крижаний дощ',
        67: 'Сильний крижаний дощ',
        71: 'Слабкий снігопад',
        73: 'Помірний снігопад',
        75: 'Сильний снігопад',
        77: 'Снігові крупинки',
        80: 'Слабка злива',
        81: 'Помірна злива',
        82: 'Сильна злива',
        85: 'Невеликий снігопад',
        86: 'Сильний снігопад',
    }
    # наша відповідь користувачеві
    print(f"Поточна погода у місті {city}:")
    # якщо статус погоди у місті є у нашому словнику з розшифровкою ...
    if current_weather['weathercode'] in weather_code:
        # ... додаємо до відповіді користувачеві статус погоди ...
        print(f"Статус: {weather_code[current_weather['weathercode']]}")
    # ... а якщо немає ...
    else:
        # пропускаємо цей крок
        pass
    # виводимо користувачеві температуру ...
    print(f"Температура: {current_weather['temperature']} °C")
    # ... та швидкість вітру
    print(f"Швидкість вітру: {current_weather['windspeed']} м/с")
# у випадку якщо місто не знайдене ...
except KeyError:
    # ...повертаємо користувачеві таку відповідь
    print(F"Місто {city} не знайдено, спробуйте ще раз.")
