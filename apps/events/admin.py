from django.contrib import admin
from django.contrib import messages
from .forms import QuestionForm
from .models import Speaker, Event, SpeakerTalk, UserProfile, Question, Donate, SendMessage


class SpeakerTalkInLine(admin.TabularInline):
    model = SpeakerTalk
    extra = 1
    search_fields = ['speaker']


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'speakers_list', 'start_event', 'end_event',)
    inlines = [SpeakerTalkInLine,]

    def speakers_list(self, obj):
      talks = obj.speakertalk_set.all()
      return ", ".join(talk.speaker.name for talk in talks)

    speakers_list.short_description = 'Спикеры'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'created_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
    list_display = ('name', 'speaker', 'is_answered', 'created_at',)
    list_filter = ('speaker', 'is_answered',)


@admin.register(Donate)
class DonateAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'created_at',)


@admin.register(SendMessage)
class SendMessageAdmin(admin.ModelAdmin):
    list_display = ('group', 'sent_at', 'is_sent')
    fields = ('group', 'message')

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
                