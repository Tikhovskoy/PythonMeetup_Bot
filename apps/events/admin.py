from django import forms
from django.contrib import admin, messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.http import HttpResponseRedirect
from django.shortcuts import render

from bot.services.send_message_service import send_telegram_message

from .forms import QuestionForm
from .models import (Donate, Event, Question, SendMessage, Speaker,
                     SpeakerApplication, SpeakerTalk, Subscription,
                     UserProfile)


class SpeakerTalkInLine(admin.TabularInline):
    model = SpeakerTalk
    extra = 1
    search_fields = ["speaker"]


class SendSpeakerMessageForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    message = forms.CharField(
        widget=forms.Textarea, label="Текст сообщения для авторов заявок"
    )


def send_message_to_applicants(modeladmin, request, queryset):
    if "apply" in request.POST:
        request.POST = request.POST.copy()
        request.POST["action"] = "send_message_to_applicants"
        form = SendSpeakerMessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            count = 0
            for obj in queryset:
                send_telegram_message(obj.telegram_id, message)
                count += 1
            modeladmin.message_user(
                request, f"Сообщение отправлено {count} авторам заявок."
            )
            return HttpResponseRedirect(request.get_full_path())
    else:
        form = SendSpeakerMessageForm(
            initial={"_selected_action": request.POST.getlist(ACTION_CHECKBOX_NAME)}
        )
    return render(
        request,
        "admin/send_speaker_message.html",
        {
            "form": form,
            "objects": queryset,
            "action": "send_message_to_applicants",
        },
    )


send_message_to_applicants.short_description = (
    "Отправить сообщение авторам выбранных заявок"
)


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "speakers_list", "start_event", "end_event")
    search_fields = ("title",)
    inlines = [SpeakerTalkInLine]

    def speakers_list(self, obj):
        talks = obj.speakertalk_set.all()
        return ", ".join(talk.speaker.name for talk in talks)

    speakers_list.short_description = "Спикеры"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "grade", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
    list_display = ("name", "speaker", "is_answered", "created_at")
    list_filter = ("speaker", "is_answered")
    search_fields = ("name",)
    readonly_fields = ("created_at",)


@admin.register(Donate)
class DonateAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "formatted_amount", "created_at")
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
    list_display = ("telegram_id", "is_subscribed", "created_at")
    list_filter = ("is_subscribed",)
    readonly_fields = ("created_at",)


@admin.register(SpeakerApplication)
class SpeakerApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "topic", "status", "created_at")
    list_filter = ("status",)
    search_fields = (
        "name",
        "topic",
    )
    readonly_fields = ("created_at",)
    actions = [send_message_to_applicants]
