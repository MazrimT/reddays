from flask import Blueprint, render_template, request
import requests
import json
from datetime import datetime




index = Blueprint('index', __name__)

def get_days(year, show_weekend=False):
    base_url = 'http://sholiday.faboul.se/dagar/v2.1/'
    days = json.loads(requests.get(f"{base_url}{year}").text)['dagar']

    days = [
        {
            "date": day['datum'],
            "red": True if day['röd dag'] == 'Ja' else False,
            "workfree": True if day['arbetsfri dag'] == 'Ja' else False,
            "holiday": day['helgdag'] if "helgdag" in day else "",
            "day_of_week": int(day['dag i vecka']),
            "weekday": day['veckodag'],
            "week": day['vecka'],
            "flag": True if day['flaggdag'] else False,
            "flag_reason": day['flaggdag']
        }
        for day in days
    ]

 
    if show_weekend:
        return [day for day in days if (day['day_of_week'] < 6 and day['workfree']) or (day['red'] and day["holiday"])]
    else:
        return [day for day in days if day['day_of_week'] < 6 and day['workfree']]


@index.route('/', methods=["POST", "GET"])
def v_index():

    current_year = str(datetime.now().year)
    years = [str(year) for year in range(datetime.now().year-10, datetime.now().year+10)]
 
    year = current_year if request.method == 'GET' else request.form["year"] 

    show_weekend = False if request.method == 'GET' or (request.method == 'POST' and "checkbox" in request.form.keys()) else True
    days = get_days(year, show_weekend)

    has_none_red = True if False in [day['red'] for day in days] else False

    

    return render_template('index.html', days=days, default_year=year, current_year=current_year, years=years, show_weekend=show_weekend, has_none_red=has_none_red)
    
