from django.contrib import admin

from .models import Speaker, Event


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_speakers', 'start_event', 'end_event',)
    filter_horizontal = ['speakers']

    def get_speakers(self, obj):
        return ", ".join([speaker.name for speaker in obj.speakers.all()])

    get_speakers.short_description = 'Докладчики'

