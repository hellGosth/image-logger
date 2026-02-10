import celery
import geoip2.database
from user_agents import parse
import requests

app = celery.Celery('tasks', broker='redis://localhost:6379/0')

# GeoIP Task
@app.task
def get_geoip(ip_address):
    try:
        reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        response = reader.city(ip_address)
        return {
            'ip': ip_address,
            'city': response.city.name,
            'country': response.country.name,
            'latitude': response.location.latitude,
            'longitude': response.location.longitude
        }
    except Exception as e:
        return {'error': str(e)}

# User-Agent Detection Task
@app.task
def get_user_agent_info(user_agent_string):
    user_agent = parse(user_agent_string)
    return {
        'browser': user_agent.browser.family,
        'platform': user_agent.os.family,
        'is_mobile': user_agent.is_mobile,
        'is_tablet': user_agent.is_tablet
    }

# Sherlock Task for username detection
@app.task
def find_username(username):
    url = f'https://sherlock-project.github.io/sherlock/{username}'
    response = requests.get(url)
    return response.text