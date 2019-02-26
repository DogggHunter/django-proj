from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Test, Question, TestRun, TestRunAnswers
from .mixins import NoteViewMixin
from .forms import TestRunAnswersForm
from django.forms import formset_factory


class IndexListView(ListView):
    model = Test
    context_object_name = 'tests'
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        searched_word = self.request.POST['find_text']
        tests = Test.objects.all().filter(name__contains=searched_word) or \
            Test.objects.all().filter(description__contains=searched_word)
        return render(request, self.template_name, context={'tests': tests, 'searched_word': searched_word})


class TestDetailView(NoteViewMixin):
    model = Test
    context_object_name = 'test'
    template_name = 'tests/detail.html'


class TestCreateView(CreateView):
    model = Test
    fields = ['name', 'description', 'questions']
    template_name = 'tests/create.html'
    success_url = reverse_lazy('index')


class TestUpdateView(UpdateView):
    model = Test
    fields = ['name', 'description', 'questions']
    template_name = 'tests/update.html'

    def get_success_url(self):
        return reverse_lazy('testing_app:test', kwargs={'pk': self.get_object().id})


class TestDeleteView(DeleteView):
    model = Test
    context_object_name = 'test'
    template_name = 'tests/delete.html'
    success_url = reverse_lazy('index')


class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'questions/detail.html'


class QuestionCreateView(CreateView):
    model = Question
    fields = ['description']
    template_name = 'questions/create.html'
    success_url = reverse_lazy('index')


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['description']
    template_name = 'questions/update.html'

    def get_success_url(self):
        return reverse_lazy('testing_app:question', kwargs={'pk': self.get_object().id})


class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'questions/delete.html'
    success_url = reverse_lazy('index')


class TestPassageDetailView(DetailView):
    model = Test
    context_object_name = 'test'
    template_name = 'tests/run.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = self.get_object().questions.all()
        formset = formset_factory(TestRunAnswersForm, min_num=questions.count())()
        context['formset'] = dict(zip(questions, formset))
        context['management_form'] = formset.management_form
        return context

    def post(self, request, *args, **kwargs):
        questions = self.get_object().questions.all()
        formset = formset_factory(TestRunAnswersForm, min_num=questions.count())(request.POST)
        if formset.is_valid():
            answers = dict(zip(questions, formset.cleaned_data))
            test_run = TestRun.objects.create(test=self.get_object())
            for question, answer in answers.items():
                TestRunAnswers.objects.create(test_run=test_run,
                                              question=question,
                                              answer=answer['answer'])
        return redirect(reverse('testing_app:testruns'))


class TestRunDetailView(NoteViewMixin):
    model = TestRun
    context_object_name = 'test_run'
    template_name = 'test_runs/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = TestRunAnswers.objects.select_related('question').filter(test_run=self.object)
        return context


class TestRunsListView(ListView):
    model = TestRun
    context_object_name = 'test_runs'
    template_name = "test_runs/index.html"

    def get_queryset(self):
        return self.model.objects.select_related('test').all().order_by('-created_on')

