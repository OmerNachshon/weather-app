"""
Utility functions for the Weather Forecast App
"""
import requests
from flask import current_app


class WeatherAPIError(Exception):
    """Custom exception for weather API errors"""
    pass


def fetch_weather_data(city, timeout=10):
    """
    Fetch weather data from OpenWeather API
    
    Args:
        city (str): Name of the city
        timeout (int): Request timeout in seconds
        
    Returns:
        tuple: (forecasts_list, error_message)
        
    Raises:
        WeatherAPIError: When API request fails
    """
    api_key = current_app.config.get('OPENWEATHER_API_KEY')
    
    if not api_key:
        return None, "OpenWeather API key not configured"
    
    if not city or not city.strip():
        return None, "City name is required"
    
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast"
        params = {
            'q': city.strip(),
            'appid': api_key,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params, timeout=timeout)
        data = response.json()
        
        if response.status_code != 200 or data.get('cod') != '200':
            error_msg = data.get('message', 'City not found or API error')
            return None, error_msg
        
        # Return only the first 5 forecasts
        forecasts = data.get('list', [])[:5]
        
        if not forecasts:
            return None, "No forecast data available"
            
        return forecasts, None
        
    except requests.exceptions.Timeout:
        return None, "Weather service timeout - please try again"
    except requests.exceptions.ConnectionError:
        return None, "Unable to connect to weather service"
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Weather API request error: {e}")
        return None, "Error contacting weather service"
    except Exception as e:
        current_app.logger.error(f"Unexpected weather API error: {e}")
        return None, "Internal server error"


def validate_weather_data(weather_data):
    """
    Validate weather forecast data structure
    
    Args:
        weather_data: Data to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not weather_data:
        return False
        
    if not isinstance(weather_data, list):
        return False
        
    if len(weather_data) == 0:
        return False
        
    # Check if each forecast item has required fields
    required_fields = ['dt_txt', 'main', 'weather']
    
    for item in weather_data:
        if not isinstance(item, dict):
            return False
            
        for field in required_fields:
            if field not in item:
                return False
                
        # Check main weather data
        if not isinstance(item.get('main'), dict):
            return False
            
        if 'temp' not in item['main']:
            return False
            
        # Check weather array
        weather_array = item.get('weather')
        if not isinstance(weather_array, list) or len(weather_array) == 0:
            return False
            
        weather_info = weather_array[0]
        if not isinstance(weather_info, dict):
            return False
            
        if 'description' not in weather_info:
            return False
    
    return True


def format_forecast_summary(weather_item):
    """
    Create a summary string for a weather forecast item
    
    Args:
        weather_item (dict): Single weather forecast item
        
    Returns:
        str: Formatted summary
    """
    try:
        temp = weather_item['main']['temp']
        description = weather_item['weather'][0]['description']
        return f"{temp:.1f}°C, {description.title()}"
    except (KeyError, IndexError, TypeError):
        return "Data unavailable"


def get_weather_icon_url(icon_code, size='2x'):
    """
    Generate weather icon URL from OpenWeather icon code
    
    Args:
        icon_code (str): Weather icon code from API
        size (str): Icon size ('1x', '2x', '4x')
        
    Returns:
        str: Complete icon URL
    """
    if not icon_code:
        return ""
        
    return f"https://openweathermap.org/img/wn/{icon_code}@{size}.png"
