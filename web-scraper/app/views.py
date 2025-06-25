from flask import Blueprint, request,jsonify
from redbeat import RedBeatSchedulerEntry
from redbeat.schedules import rrule
from datetime import datetime
from celery import current_app as celery_app

from uuid import uuid4

from .tasks import my_task

main = Blueprint("main", __name__)

@main.route("/scrape", methods=["POST"])
def index():
    data = request.json

    url = data.get('url')
    schedule_time = data.get("schedule_time", 5)
    interval_str = data.get("interval", "MINUTELY")
    interval = get_time_interval(interval_str)
    print(f"Scraping {url} schedule_time {schedule_time} interval {interval}")

    if not url:
        return jsonify({"error": "URL is required"}), 400
    if interval == "Invalid interval":
        return jsonify({"error": "Interval is out of scope"}), 400

    schedule_name = str(uuid4())
    dt = datetime.utcnow()
    interval_rrule = rrule(
        freq=interval,
        interval=schedule_time,
        dtstart=dt
    )

    entry = RedBeatSchedulerEntry(
        schedule_name,
        "app.tasks.my_task",
        interval_rrule,
        args=["From the scheduler"],
        kwargs={"schedule_name": schedule_name, "Site_url": url},
        app=celery_app
    )
    entry.save()

    return jsonify({
        "task_id": schedule_name,
        "status": "queued",
        "Intervals": schedule_time
    }), 202




def get_time_interval(interval):
    match interval.upper():
        case "Y":
            return "YEARLY"
        case "M":
            return "MONTHLY"
        case "W":
            return "WEEKLY"
        case "D":
            return "DAILY"
        case "HOUR":
            return "HOURLY"
        case "MIN":
            return "MINUTELY"
        case "SEC":
            return "SECONDLY"
        case _:
            return "Invalid interval"


