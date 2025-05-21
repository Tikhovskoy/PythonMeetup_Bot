from django.contrib import admin

from .models import Speaker, Event, SpeakerTalk


class SpeakerTalkInLine(admin.TabularInline):
    model = SpeakerTalk
    extra = 1
    search_fields = ['speaker']


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'speakers_list', 'start_event', 'end_event',)
    inlines = [SpeakerTalkInLine,]

    def speakers_list(self, obj):
      talks = obj.speakertalk_set.all()
      return ", ".join(talk.speaker.name for talk in talks)

    speakers_list.short_description = 'Спикеры'

