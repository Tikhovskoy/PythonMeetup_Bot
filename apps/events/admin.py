from django.contrib import admin, messages

from .forms import QuestionForm
from .models import (Donate, Event, Question, SendMessage, Speaker,
                     SpeakerApplication, SpeakerTalk, Subscription,
                     UserProfile)


class SpeakerTalkInLine(admin.TabularInline):
    model = SpeakerTalk
    extra = 1
    search_fields = ["speaker"]


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
    )
    search_fields = ("name",)
    readonly_fields = ("created_at",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "speakers_list",
        "start_event",
        "end_event",
    )
    search_fields = ("title",)
    inlines = [
        SpeakerTalkInLine,
    ]

    def speakers_list(self, obj):
        talks = obj.speakertalk_set.all()
        return ", ".join(talk.speaker.name for talk in talks)

    speakers_list.short_description = "Спикеры"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "grade",
        "created_at",
    )
    search_fields = ("name",)
    readonly_fields = ("created_at",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
    list_display = (
        "name",
        "speaker",
        "is_answered",
        "created_at",
    )
    list_filter = (
        "speaker",
        "is_answered",
    )
    search_fields = ("name",)
    readonly_fields = ("created_at",)


@admin.register(Donate)
class DonateAdmin(admin.ModelAdmin):
    list_display = (
        "telegram_id",
        "formatted_amount",
        "created_at",
    )
    readonly_fields = ("created_at",)

    def formatted_amount(self, obj):
        return f"{obj.amount} ₽"

    formatted_amount.short_description = "Сумма доната"


@admin.register(SendMessage)
class SendMessageAdmin(admin.ModelAdmin):
    list_display = ("group", "sent_at", "is_sent")
    fields = ("group", "message")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            errors = []
            try:
                obj.send_messages()
            except Exception as e:
                errors.append(str(e))
            if errors:
                for error in errors:
                    messages.error(request, error)
            else:
                messages.success(request, "Сообщения успешно отправлены")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "telegram_id",
        "is_subscribed",
        "created_at",
    )
    list_filter = ("is_subscribed",)
    readonly_fields = ("created_at",)


@admin.register(SpeakerApplication)
class SpeakerApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "topic",
        "status",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = (
        "name",
        "topic",
    )
    readonly_fields = ("created_at",)
