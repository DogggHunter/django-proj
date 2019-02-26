from django.test import TestCase
from .models import Test, Question, TestRun
from django.urls import reverse
from .forms import TestRunAnswersForm
from django.forms import formset_factory


class TestTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for i in range(3):
            Question.objects.create(description="TestQuestion")

    def test_create(self):
        data = {
            'name': 'Test1',
            'description': 'About test1',
            'questions': Question.objects.values_list('pk', flat=True)
        }
        self.client.post(reverse('testing_app:test_create'), data)
        self.assertEqual(Test.objects.count(), 1)

    def test_add_question(self):
        test = Test.objects.create(name='Test1', description='About test1')
        data = {
            'name': test.name,
            'description': test.description,
            'questions': Question.objects.get(pk=1).pk
        }
        self.client.post(reverse('testing_app:test_update', kwargs={'pk': test.pk}), data)
        self.assertEqual(test.questions.count(), 1)


class TestRunTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for i in range(3):
            Question.objects.create(description="TestQuestion")

        cls.test = Test.objects.create(name='Test1', description='About Test1')
        cls.test.questions.set(Question.objects.all())
        cls.formset_factory = formset_factory(TestRunAnswersForm, min_num=3)
        cls.data = {
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '2',
            'form-MAX_NUM_FORMS': '1000',
        }

    def testrun_passage(self):
        answers = {
            'form-0-answer': 'Answer1',
            'form-1-answer': 'Answer2',
            'form-2-answer': 'Answer3',
        }
        data = {**self.data, **answers}
        formset = self.formset_factory(data)
        self.assertTrue(formset.is_valid())

        self.client.post(reverse('testing_app:test_run', kwargs={'pk': self.test.pk}), data)
        self.assertEqual(TestRun.objects.count(), 1)

    def testrun_failed(self):
        answers = {
            'form-0-answer': '',
            'form-1-answer': '',
            'form-2-answer': '',
        }
        data = {**self.data, **answers}
        formset = self.formset_factory(data)
        self.assertFalse(formset.is_valid())
