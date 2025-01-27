from django.contrib import admin
from django.urls import path, include

from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime, timedelta
from typing import Callable

from collaboration.jobs.snapshot_job import snapshot_job

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/c/", include("collaboration.urls")),
]
scheduler = BackgroundScheduler()


def schedule_next_execution(
    function: Callable[[], None], interval_in_secs: int = 20
) -> None:
    now = datetime.now()
    next_run_time = now + timedelta(seconds=interval_in_secs)

    print(f"Next job will run at {next_run_time}")

    def wrapper_function():
        function()
        schedule_next_execution(function=function, interval_in_secs=interval_in_secs)

    scheduler.add_job(wrapper_function, "date", run_date=next_run_time)


schedule_next_execution(function=snapshot_job)

try:
    # scheduler.start()
    pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler stopped.")
