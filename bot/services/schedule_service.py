from typing import Dict, List

from asgiref.sync import sync_to_async

from apps.events.models import Event
from bot.logging_tools import logger


@sync_to_async
def get_schedule() -> List[Dict]:
    events = Event.objects.prefetch_related("speakertalk_set__speaker").order_by(
        "start_event"
    )
    logger.info("Получено расписание мероприятий (%s событий)", events.count())
    schedule = []
    for event in events:
        event_data = {
            "title": event.title,
            "description": event.description or "",
            "start_event": (
                event.start_event.strftime("%H:%M") if event.start_event else ""
            ),
            "end_event": event.end_event.strftime("%H:%M") if event.end_event else "",
            "date": event.start_event.strftime("%d.%m.%Y") if event.start_event else "",
            "talks": [],
        }
        talks = event.speakertalk_set.all().order_by("start_performance")
        for talk in talks:
            event_data["talks"].append(
                {
                    "time": (
                        talk.start_performance.strftime("%H:%M")
                        if talk.start_performance
                        else ""
                    ),
                    "speaker": talk.speaker.name if talk.speaker else "",
                    "topic": talk.topic or "",
                }
            )
        schedule.append(event_data)
    return schedule
