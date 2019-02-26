from django.forms import ModelForm
from .models import TestRunAnswers
from django.forms import TextInput


class TestRunAnswersForm(ModelForm):
    class Meta:
        model = TestRunAnswers
        fields = ('answer', )
        widgets = {
            'answer': TextInput(attrs={'required': 'true'})
        }
