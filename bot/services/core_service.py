from datetime import datetime


async def register_user(user_id):
    # Пока просто мок — потом добавим реальную логику регистрации
    print(f"Register user: {user_id}")


def is_speaker(user_id: int) -> bool:
    # Запрос в бд
    SPEAKER = {"id": 105718620}
    return user_id == SPEAKER.get("id")


def event_schedule(name):
    # Тестовые
    MOCK_SCHEDULE = [
        {"speaker": {"started_at": "12:00", "ended_at": "14:00", "name": "Иван Иванов", "topic": "Python и нейросети"}},
        {"speaker": {"started_at": "22:30", "ended_at": "23:45", "name": "Роман", "topic": "Асинхронность в Python"}},
    ]

    now = datetime.now()
    text = ""
    for event in MOCK_SCHEDULE:
        speaker = event.get("speaker")
        if speaker.get("name") == name:
            start_at = speaker.get("started_at")
            end_at = speaker.get("ended_at")
            start_time = datetime.strptime(start_at, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )
            time_to_start = start_time - now
            if time_to_start.total_seconds() > 0:
                time_left = str(time_to_start).split('.')[0]
                text += (
                    "Ваше время выступления\n"
                    f"Начало: {start_at}\n"
                    f"Конец:  {end_at}\n"
                    f"До начала: {time_left}\n"
                )
            else:
                text += (
                    f"Выступление '{speaker.get('topic')}' у {name} уже началось.\n"
                    f"Начало: {start_at}\n"
                    f"Конец:  {end_at}\n"
                )
    return text
