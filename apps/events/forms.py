from django import forms
from django.utils import timezone
from .models import Question, SpeakerTalk


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        self.fields['speaker'].queryset = SpeakerTalk.objects.filter(
            start_performance__lte=now,
            end_performance__gte=now
        )
