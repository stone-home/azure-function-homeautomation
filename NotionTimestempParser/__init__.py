import datetime
import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    payload = req.get_json()
    input_date = payload.get("date")
    logging.info('Python HTTP trigger function processed a request.')

    time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    date_format = "%Y-%m-%d"

    try:
        out = datetime.datetime.strptime(input_date, time_format)
        output = {
            "year": out.year,
            "month": out.month,
            "day": out.day,
            "hour": out.hour,
            "minute": out.minute,
            "second": out.second,
            "include_time": True
        }
    except ValueError:
        out = datetime.datetime.strptime(input_date, date_format)
        output = {
            "year": out.year,
            "month": out.month,
            "day": out.day,
            "include_time": False
        }
    finally:
        return func.HttpResponse(json.dumps(output), mimetype="application/json", status_code=200)
