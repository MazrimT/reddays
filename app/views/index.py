from flask import Blueprint, render_template, request
import requests
import json
from datetime import datetime




index = Blueprint('index', __name__)

def get_days(year: str,) -> list:
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
            "flag_reason": day['flaggdag'],
            "is_none_work_day": True if day['röd dag'] == 'Ja' or day.get("helgdag") or int(day['dag i vecka']) >= 6 or day['arbetsfri dag'] == 'Ja' else False,
        }
        for day in days
    ]


    return days


def get_squeeze_days(days:list) -> list:

    squeeze_days = []

    for i, day in enumerate(days):
        squeeze_day_reasons = []
        if not day["is_none_work_day"]:

            # "today" is a workday yesterday and tomorrow are not
            if days[i-1]["is_none_work_day"] and days[i+1]["is_none_work_day"]:


                if days[i-1]["holiday"]:
                    squeeze_day_reasons.append(f'{days[i-1]["date"]} - {days[i-1]["holiday"]}')
                else:
                    squeeze_day_reasons.append(f'{days[i-1]["date"]} - {days[i-1]["weekday"]}')

                if days[i+1]["holiday"]:
                    squeeze_day_reasons.append(f'{days[i+1]["date"]} - {days[i+1]["holiday"]}')
                else:
                    squeeze_day_reasons.append(f'{days[i+1]["date"]} - {days[i+1]["weekday"]}')

                day["squeeze_day_reasons"] = " | ".join(squeeze_day_reasons)
                day["squeeze_day_type"] = "Enkel"
                squeeze_days.append(day)

            # "today" and yesterday is a workday but two days ago is not and tomorrow is not
            elif not days[i-1]["is_none_work_day"] and days[i-2]["is_none_work_day"] and days[i+1]["is_none_work_day"] and day not in squeeze_days:

                if days[i-2]["holiday"]:
                    squeeze_day_reasons.append(f'{days[i-2]["date"]} - {days[i-2]["holiday"]}')
                else:
                    squeeze_day_reasons.append(f'{days[i-2]["date"]} - {days[i-2]["weekday"]}')

                if days[i+1]["holiday"]:
                    squeeze_day_reasons.append(f'{days[i+1]["date"]} - {days[i+1]["holiday"]}')
                else:
                    squeeze_day_reasons.append(f'{days[i+1]["date"]} - {days[i+1]["weekday"]}')


                day["squeeze_day_reasons"] = " | ".join(squeeze_day_reasons)
                day["squeeze_day_type"] = "Dubbel"
                squeeze_days.append(day)

            # "today" and tomorrow is a workday but two days in the future is not and yesterday is not
            elif not days[i+1]["is_none_work_day"] and days[i+2]["is_none_work_day"] and days[i-1]["is_none_work_day"] and day not in squeeze_days:

                if days[i-1]["holiday"]:
                    squeeze_day_reasons.append(f'{days[i-1]["date"]} - {days[i-1]["holiday"]}')
                else:
                    squeeze_day_reasons.append(f'{days[i-1]["date"]} - {days[i-1]["weekday"]}')

                if days[i+2]["holiday"]:
                    squeeze_day_reasons.append(f'{days[i+2]["date"]} - {days[i+2]["holiday"]}')
                else:
                    squeeze_day_reasons.append(f'{days[i+2]["date"]} - {days[i+2]["weekday"]}')

                day["squeeze_day_reasons"] = " | ".join(squeeze_day_reasons)
                day["squeeze_day_type"] = "Dubbel"
                squeeze_days.append(day)

        # make sure list is in date order
        squeeze_days =  sorted(squeeze_days, key=lambda x: x['date'])
    return squeeze_days


@index.route('/', methods=["POST", "GET"])
def v_index():

    current_year = str(datetime.now().year)
    years = [str(year) for year in range(datetime.now().year-10, datetime.now().year+10)]

    year = current_year if request.method == 'GET' else request.form["year"]

    show_weekend = False if request.method == 'GET' or (request.method == 'POST' and "checkbox" in request.form.keys()) else True
    days = get_days(year)


    if show_weekend:
        display_days = [day for day in days if (day['day_of_week'] < 6 and day['workfree']) or (day['red'] and day["holiday"])]
    else:
        display_days = [day for day in days if day['day_of_week'] < 6 and day['workfree']]

    has_none_red = True if False in [day['red'] for day in display_days] else False

    squeeze_days = get_squeeze_days(days)

    return render_template(
        'index.html',
        days=display_days,
        default_year=year,
        current_year=current_year,
        years=years,
        show_weekend=show_weekend,
        has_none_red=has_none_red,
        squeeze_days=squeeze_days,
    )
