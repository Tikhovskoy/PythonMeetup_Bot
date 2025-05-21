from django.db import models


class Speaker(models.Model):
    name = models.CharField(verbose_name='Ф.И.О', max_length=100)
    biography = models.TextField(verbose_name='Биография', null=True, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Описание мероприятия', null=True, blank=True)
    start_event = models.DateTimeField(verbose_name='Начало мероприятия', null=True, blank=True)
    end_event = models.DateTimeField(verbose_name='Конец мероприятия', null=True, blank=True)

    def __str__(self):
        return self.title


class SpeakerTalk(models.Model):
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE, verbose_name='Докладчики')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    start_performance = models.DateTimeField(verbose_name='Начало выступления', null=True, blank=True)
    end_performance = models.DateTimeField(verbose_name='Конец выступления', null=True, blank=True)

    def __str__(self):
        return self.speaker.name





