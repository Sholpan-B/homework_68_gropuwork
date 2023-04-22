from django import forms
from django.forms import TextInput

from job.models import Education, WorkExperience, Resume


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('title', 'first_name', 'last_name', 'position', 'category', 'salary', 'telegram',
                  'email', 'phone_number', 'facebook', 'linkedin')


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ('university', 'start_date', 'end_date', 'major', 'location',)
        widgets = {
            'start_date': TextInput(attrs={'class': 'form-control', 'style': 'max-width: 400px;', 'type': 'date'}),
            'end_date': TextInput(attrs={'class': 'form-control', 'style': 'max-width: 400px;', 'type': 'date'})
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ('company_name', 'start_date', 'end_date', 'position', 'responsibilities')
        widgets = {
            'start_date': TextInput(attrs={'class': 'form-control', 'style': 'max-width: 400px;', 'type': 'date'}),
            'end_date': TextInput(attrs={'class': 'form-control', 'style': 'max-width: 400px;', 'type': 'date'})
        }
