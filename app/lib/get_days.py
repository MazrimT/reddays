import requests
import json

def get_days(year, all_days=False):
    base_url = 'http://sholiday.faboul.se/dagar/v2.1/'
    days = json.loads(requests.get(f"{base_url}{year}").text)['dagar']

    return [day for day in days if int(day['dag i vecka']) < 6 and day['arbetsfri dag'] == 'Ja']
