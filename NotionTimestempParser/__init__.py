import datetime
import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    payload = req.get_json()
    logging.info('Python HTTP trigger function processed a request.')
    output = {}
    
    start = payload.get("start", None)
    end = payload.get("end", None)
    if start is None:
        func.HttpResponse("start field is mandatory", status_code=400)
    
    #process start date
    start_dict, start_dt = parse_notion_date(start)

    if end is None:
        if start_dict['allday'] is True:
            end_dt = start_dt
        else:
            delta_hour = datetime.timedelta(hours=1)
            end_dt = start_dt + delta_hour
    else:
        end_dict, end_dt = parse_notion_date(end)
    

    output = {
        "start": start_dt.strftime(start_dict['format']),
        "end": end_dt.strftime(start_dict['format']),
        "allday": start_dict['allday']
    }
        
    return func.HttpResponse(json.dumps(output), mimetype="application/json", status_code=200)


def parse_notion_date(date: str):
    # notion format: 2022-11-19T00:00:00.000+08:00
    time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    date_format = "%Y-%m-%d"
    google_format = "%Y-%m-%d %H:%M:%S GMT+08:00"
    try:
        out = datetime.datetime.strptime(date, time_format)
        output = {
            "format": google_format,
            "year": out.year,
            "month": out.month,
            "day": out.day,
            "hour": out.hour,
            "minute": out.minute,
            "second": out.second,
            "allday": False
        }
    except ValueError:
        out = datetime.datetime.strptime(date, date_format)
        output = {
            "format": date_format,
            "year": out.year,
            "month": out.month,
            "day": out.day,
            "allday": True
        }
    finally:
        return output, out

