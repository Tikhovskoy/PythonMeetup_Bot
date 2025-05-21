from django.db import models


class Speaker(models.Model):
    name = models.CharField(verbose_name='Ф.И.О', max_length=100)
    biography = models.TextField(verbose_name='Биография', null=True, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)
    speakers = models.ManyToManyField('Speaker', related_name='events', verbose_name='Докладчики')
    description = models.TextField(verbose_name='Описание мероприятия', null=True, blank=True)
    start_event = models.DateTimeField(verbose_name='Начало мероприятия', null=True, blank=True)
    end_event = models.DateTimeField(verbose_name='Конец мероприятия', null=True, blank=True)

    def __str__(self):
        return self.title





