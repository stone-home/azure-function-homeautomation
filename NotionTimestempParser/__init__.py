import datetime
import logging
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    s = req.get_json()
    logging.info('Python HTTP trigger function processed a request.')

    time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    date_format = "%Y-%m-%d"

    try:
        out = datetime.datetime.strptime(s, time_format)
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
        out = datetime.datetime.strptime(s, date_format)
        output = {
            "year": out.year,
            "month": out.month,
            "day": out.day,
            "include_time": False
        }
    finally:
        return func.HttpResponse(output, status_code=200)
