from django import forms
from django.forms import Textarea

from job.models import Response, ResponseMessage, Vacancy


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('location', 'position', 'category', 'salary', 'description', 'experience_from', 'experience_to')


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('vacancy', 'resume',)


class ResponseMessageForm(forms.ModelForm):
    class Meta:
        model = ResponseMessage
        fields = ('text',)
        labels = {'text': ''}
        widgets = {
            'text': Textarea(attrs={
                'rows': 4,
                'cols': 38,
                'placeholder': 'Type a message',
                'class': 'border-0 border-top rounded',
                'style': 'outline:0px none transparent; overflow:auto; resize:none',
            })
        }

