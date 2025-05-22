from apps.events.models import Event, SpeakerTalk
from typing import List, Dict
from asgiref.sync import sync_to_async

@sync_to_async
def get_schedule() -> List[Dict]:
    """
    Возвращает расписание всех мероприятий с докладчиками и докладами.
    """
    events = (
        Event.objects
        .prefetch_related('speakertalk_set__speaker')
        .order_by('start_event')
    )
    schedule = []
    for event in events:
        talks = event.speakertalk_set.all()
        if talks.exists():
            for talk in talks:
                schedule.append({
                    "time": talk.start_performance.strftime("%H:%M") if talk.start_performance else "",
                    "speaker": talk.speaker.name if talk.speaker else "",
                    "topic": event.title,
                })
        else:
            # Мероприятие без спикера 
            schedule.append({
                "time": event.start_event.strftime("%H:%M") if event.start_event else "",
                "speaker": "",
                "topic": event.title,
            })
    return schedule
