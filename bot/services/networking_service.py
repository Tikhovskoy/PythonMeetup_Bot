from typing import Optional, List
from asgiref.sync import sync_to_async
from apps.events.models import UserProfile 

def validate_profile_data(data: dict) -> Optional[str]:
    required_fields = ['name', 'contacts', 'stack', 'role', 'grade']
    for field in required_fields:
        value = data.get(field, '').strip()
        if not value:
            return f"Поле «{field}» обязательно для заполнения."
        if len(value) < 2:
            return f"Поле «{field}» слишком короткое."
    return None

@sync_to_async
def save_profile(telegram_id: int, data: dict) -> dict:
    error = validate_profile_data(data)
    if error:
        raise ValueError(error)
    profile, created = UserProfile.objects.update_or_create(
        telegram_id=telegram_id,
        defaults={
            'name': data['name'].strip(),
            'contacts': data['contacts'].strip(),
            'stack': data['stack'].strip(),
            'role': data['role'].strip(),
            'grade': data['grade'].strip(),
        }
    )
    return {
        'telegram_id': profile.telegram_id,
        'name': profile.name,
        'contacts': profile.contacts,
        'stack': profile.stack,
        'role': profile.role,
        'grade': profile.grade,
        'created_at': profile.created_at.isoformat(),
    }

@sync_to_async
def get_profile(telegram_id: int) -> Optional[dict]:
    try:
        profile = UserProfile.objects.get(telegram_id=telegram_id)
        return {
            'telegram_id': profile.telegram_id,
            'name': profile.name,
            'contacts': profile.contacts,
            'stack': profile.stack,
            'role': profile.role,
            'grade': profile.grade,
            'created_at': profile.created_at.isoformat(),
        }
    except UserProfile.DoesNotExist:
        return None

@sync_to_async
def get_random_profile(exclude_telegram_id: int) -> Optional[dict]:
    from random import choice
    profiles = UserProfile.objects.exclude(telegram_id=exclude_telegram_id)
    count = profiles.count()
    if not count:
        return None
    profile = choice(list(profiles))
    return {
        'telegram_id': profile.telegram_id,
        'name': profile.name,
        'contacts': profile.contacts,
        'stack': profile.stack,
        'role': profile.role,
        'grade': profile.grade,
        'created_at': profile.created_at.isoformat(),
    }

@sync_to_async
def get_profiles_list(exclude_telegram_id: int, exclude_list: Optional[List[int]] = None) -> List[dict]:
    exclude_list = exclude_list or []
    profiles = UserProfile.objects.exclude(telegram_id=exclude_telegram_id).exclude(telegram_id__in=exclude_list)
    return [
        {
            'telegram_id': profile.telegram_id,
            'name': profile.name,
            'contacts': profile.contacts,
            'stack': profile.stack,
            'role': profile.role,
            'grade': profile.grade,
            'created_at': profile.created_at.isoformat(),
        }
        for profile in profiles
    ]

@sync_to_async
def get_profiles_count() -> int:
    return UserProfile.objects.count()
