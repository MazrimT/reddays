from flask import Blueprint, render_template, request
import requests
import json
from datetime import datetime




index = Blueprint('index', __name__)

def get_days(year, all_days=False):
    base_url = 'http://sholiday.faboul.se/dagar/v2.1/'
    days = json.loads(requests.get(f"{base_url}{year}").text)['dagar']

    return [day for day in days if int(day['dag i vecka']) < 6 and day['arbetsfri dag'] == 'Ja']


@index.route('/', methods=["POST", "GET"])
def v_index():

    current_year = str(datetime.now().year)
    years = [str(year) for year in range(datetime.now().year-10, datetime.now().year+10)]
 
    year = current_year if request.method == 'GET' else request.form["year"] 

    days = get_days(year)

    return render_template('index.html', days=days, default_year=year, current_year=current_year, years=years)
    
