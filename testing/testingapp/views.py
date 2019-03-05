from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Test, Question, TestRun, TestRunAnswers
from .mixins import NoteViewMixin
from .forms import TestRunAnswersForm
from django.forms import formset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


class IsOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().author

    def handle_no_permission(self):
        return redirect("testing_app:test", pk=self.get_object().pk)


class IsUserWhoPassedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().user

    def handle_no_permission(self):
        return redirect("testing_app:testruns")


class IsNotLoginRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('index')


class IndexListView(ListView):
    model = Test
    context_object_name = 'tests'
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        searched_word = self.request.POST['find_text']
        tests = Test.objects.all().filter(name__contains=searched_word) or \
            Test.objects.all().filter(description__contains=searched_word)
        return render(request, self.template_name, context={'tests': tests, 'searched_word': searched_word})


class TestDetailView(LoginRequiredMixin, NoteViewMixin):
    model = Test
    context_object_name = 'test'
    template_name = 'tests/detail.html'


class TestCreateView(LoginRequiredMixin, CreateView):
    model = Test
    fields = ['name', 'description', 'questions']
    template_name = 'tests/create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super(TestCreateView, self).form_valid(form)
        self.object.author = self.request.user
        self.object.save()
        return response


class TestUpdateView(IsOwnerMixin, LoginRequiredMixin, UpdateView):
    model = Test
    fields = ['name', 'description', 'questions']
    template_name = 'tests/update.html'

    def get_success_url(self):
        return reverse_lazy('testing_app:test', kwargs={'pk': self.object.id})


class TestDeleteView(IsOwnerMixin, LoginRequiredMixin, DeleteView):
    model = Test
    context_object_name = 'test'
    template_name = 'tests/delete.html'
    success_url = reverse_lazy('index')


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'questions/detail.html'


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['description']
    template_name = 'questions/create.html'
    success_url = reverse_lazy('index')


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['description']
    template_name = 'questions/update.html'

    def get_success_url(self):
        return reverse_lazy('testing_app:question', kwargs={'pk': self.object.id})


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'questions/delete.html'
    success_url = reverse_lazy('index')


class TestPassageDetailView(LoginRequiredMixin, DetailView):
    model = Test
    context_object_name = 'test'
    template_name = 'tests/run.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = self.object.questions.all()
        formset = formset_factory(TestRunAnswersForm, min_num=questions.count())()
        context['formset'] = dict(zip(questions, formset))
        context['management_form'] = formset.management_form
        return context

    def post(self, request, *args, **kwargs):
        questions = self.get_object().questions.all()
        formset = formset_factory(TestRunAnswersForm, min_num=questions.count())(request.POST)
        if formset.is_valid():
            answers = dict(zip(questions, formset.cleaned_data))
            test_run = TestRun.objects.create(test=self.get_object(), user=self.request.user)
            for question, answer in answers.items():
                TestRunAnswers.objects.create(test_run=test_run,
                                              question=question,
                                              answer=answer['answer'])
        return redirect(reverse('testing_app:testruns'))


class TestRunDetailView(IsUserWhoPassedMixin, LoginRequiredMixin, NoteViewMixin):
    model = TestRun
    context_object_name = 'test_run'
    template_name = 'test_runs/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = TestRunAnswers.objects.select_related('question').filter(test_run=self.object)
        return context


class TestRunsListView(LoginRequiredMixin, ListView):
    model = TestRun
    context_object_name = 'test_runs'
    template_name = "test_runs/index.html"

    def get_queryset(self):
        return self.model.objects.select_related('test').filter(user=self.request.user).order_by('-created_on')


class SignUpView(IsNotLoginRequiredMixin, FormView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return redirect('index')
