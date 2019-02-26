from django.forms import ModelForm
from .models import TestRunAnswers
from django.forms import TextInput


class TestRunAnswersForm(ModelForm):
    class Meta:
        model = TestRunAnswers
        fields = ('answer', )
        # widgets = {
        #     'answer': TextInput(attrs={'required': 'true'})
        # }

data = {
    'form-TOTAL_FORMS': '3',
    'form-INITIAL_FORMS': '0',
    'form-MIN_NUM_FORMS': '2',
    'form-MAX_NUM_FORMS': '1000',
    'form-0-answer': 'fds',
    'form-1-answer': 'fdg',
    'form-2-answer': 'fdg',
}
