# imports
import requests
import json
from datetime import datetime

# map to icons for display in widget
ICONMAP = {
  '01d':'wi-day-sunny',
  '02d':'wi-day-cloudy',
  '03d':'wi-cloudy',
  '04d':'wi-rain',
  '09d':'wi-showers',
  '10d':'wi-rain',
  '11d':'wi-thunderstorm',
  '13d':'wi-snow',
  '50d':'wi-fog',
  '01n':'wi-night-clear',
  '02n':'wi-night-cloudy',
  '03n':'wi-night-cloudy',
  '04n':'wi-night-rain',
  '09n':'wi-night-showers',
  '10n':'wi-night-rain',
  '11n':'wi-night-thunderstorm',
  '13n':'wi-night-snow',
  '50n':'wi-fog',
}

'''
This is a weather object that acts
as the mini widget on the web application
to retrieve quick stats about the queried
zipcode 

init by setting the PWOWM api key
'''
class Weather:
  
  def __init__(self):
    self.api_key = "your-weather-api-key"
    self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
  
  '''
  get the data from the server with
  the queried zipcode and parses
  the forecast and json into
  a dictionary
  @param zipcode, the query zipcode
  '''
  def update(self, city):
    try:
      # Get current weather
      params = {
        'q': city,
        'appid': self.api_key,
        'units': 'metric'
      }
      response = requests.get(self.base_url, params=params)
      data = response.json()

      if response.status_code != 200:
        return 'noData'

      # Get 5-day forecast
      forecast_response = requests.get(self.forecast_url, params=params)
      forecast_data = forecast_response.json()

      self.weather_data = {
        'current': {
          'temperature': data['main']['temp'],
          'humidity': data['main']['humidity'],
          'description': data['weather'][0]['description'],
          'wind_speed': data['wind']['speed']
        },
        'forecast': []
      }

      # Process forecast data
      for item in forecast_data['list'][:5]:
        self.weather_data['forecast'].append({
          'date': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d'),
          'temperature': item['main']['temp'],
          'description': item['weather'][0]['description']
        })

      return 'success'
    except Exception as e:
      print(f"Error: {str(e)}")
      return 'noData'
  
  '''
  return the current data
  @return data
  '''
  def display(self):
    return self.weather_data
  
  '''
  parse the owm weather object for each
  key that we have queried and then set it into
  an organized dict with its values
  @param w, pyowm weather object
  @return data as a dict
  '''
  def parse(self, w):
    temp = w.get_temperature('fahrenheit')
    if 'temp_min' in temp:
      temp = dict(day=temp['temp'],
                  min=temp['temp_min'],
                  max=temp['temp_max'])
    icon = w.get_weather_icon_name()
    
    data = dict(
      date        = dateutil.parser.parse(w.get_reference_time('iso')),
      temp        = temp.get('day', 0),
      min         = temp.get('min', 0),
      max         = temp.get('max', 0),
      wind        = w.get_wind(),
      humidity 	  = w.get_humidity(),
      status      = w.get_status(),
      pressure    = w.get_pressure(),
      description = w.get_detailed_status(),
      code        = w.get_weather_code(),
      icon        = ICONMAP.get(icon,icon),
      sunrise     = dateutil.parser.parse(w.get_sunrise_time('iso')),
      sunset      = dateutil.parser.parse(w.get_sunset_time('iso')),
    )
    return data

# tests
if __name__ == '__main__':
  weatherApp = Weather()
  weatherApp.update('Davanagere')
  data = weatherApp.display()
  for key in data:
    print (key, data[key])
