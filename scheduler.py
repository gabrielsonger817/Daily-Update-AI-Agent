import logging

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from config import UPDATE_HOUR, UPDATE_MINUTE, TIMEZONE

log = logging.getLogger(__name__)


def start_scheduler() -> None:
    tz = pytz.timezone(TIMEZONE)
    scheduler = BlockingScheduler(timezone=tz)

    # Import here to avoid circular import at module load time
    from main import run_daily_update

    scheduler.add_job(
        run_daily_update,
        trigger=CronTrigger(hour=UPDATE_HOUR, minute=UPDATE_MINUTE, timezone=tz),
        id="daily_update",
        name="Morning Daily Update",
        misfire_grace_time=300,  # allow up to 5-min late firing (e.g. after sleep/resume)
    )

    log.info(
        "Scheduler running — next briefing at %02d:%02d %s",
        UPDATE_HOUR,
        UPDATE_MINUTE,
        TIMEZONE,
    )

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info("Scheduler stopped.")
