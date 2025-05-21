import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update
from bot.handlers import networking
from bot.services import networking_service

@pytest.fixture(autouse=True)
def clear_profiles():
    networking_service._FAKE_PROFILES.clear()

@pytest.mark.asyncio
async def test_networking_three_users_flow():
    user_ids = [5555, 7777, 8888]
    profiles = [
        dict(name="Иван Петров", contacts="@ivan", stack="Python", role="Backend", grade="Junior"),
        dict(name="Мария Сидорова", contacts="@maria", stack="Django", role="Frontend", grade="Middle"),
        dict(name="Алексей Смирнов", contacts="@alex", stack="Flask", role="Fullstack", grade="Senior"),
    ]
    contexts = []
    updates = []

    # --- Все три пользователя проходят анкетирование ---
    for user_id, profile in zip(user_ids, profiles):
        context = MagicMock()
        context.user_data = {}
        update = MagicMock(spec=Update)
        update.effective_user.id = user_id
        update.message.reply_text = AsyncMock()
        await networking.networking_handler(update, context)
        update.message.text = profile['name']
        await networking.netw_name_handler(update, context)
        update.message.text = profile['contacts']
        await networking.netw_contacts_handler(update, context)
        update.message.text = profile['stack']
        await networking.netw_stack_handler(update, context)
        update.message.text = profile['role']
        await networking.netw_role_handler(update, context)
        update.message.text = profile['grade']
        await networking.netw_grade_handler(update, context)
        contexts.append(context)
        updates.append(update)

    # Проверяем, что все анкеты на месте
    for user_id, profile in zip(user_ids, profiles):
        saved = networking_service.get_profile(user_id)
        assert saved is not None
        for key in profile:
            assert saved[key] == profile[key]

    # --- Каждый пользователь листает анкеты других ---
    for idx, (context, update, user_id) in enumerate(zip(contexts, updates, user_ids)):
        # При входе в знакомства (уже после анкеты) список просмотренных пустой
        context.user_data['viewed_profiles'] = []
        show_ids = [uid for uid in user_ids if uid != user_id]
        seen = set()
        # Первое нажатие "➡️ Дальше" — показывается один из других (по алфавиту словаря)
        for _ in range(2):  # Всего 2 чужих анкеты
            # Устанавливаем current_profile_id как у show_next_profile
            next_profiles = networking_service.get_profiles_list(user_id, context.user_data['viewed_profiles'])
            if not next_profiles:
                break
            current_id = next_profiles[0]['telegram_id']
            context.user_data['current_profile_id'] = current_id
            update.message.text = "➡️ Дальше"
            await networking.netw_show_handler(update, context)
            seen.add(current_id)
            assert current_id != user_id
        # После двух нажатий "➡️ Дальше" больше новых анкет нет
        assert seen == set(show_ids)
        update.message.text = "➡️ Дальше"
        await networking.netw_show_handler(update, context)
        # Теперь можно "Начать сначала"
        update.message.text = "🔄 Начать сначала"
        await networking.netw_show_handler(update, context)
        # Можно снова листать оба профиля
        context.user_data['viewed_profiles'] = []
        for _ in range(2):
            next_profiles = networking_service.get_profiles_list(user_id, context.user_data['viewed_profiles'])
            if not next_profiles:
                break
            current_id = next_profiles[0]['telegram_id']
            context.user_data['current_profile_id'] = current_id
            update.message.text = "➡️ Дальше"
            await networking.netw_show_handler(update, context)
        update.message.text = "⬅️ В меню"
        result = await networking.netw_show_handler(update, context)
        assert result == "STATE_MENU"
