from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from .models import Test


class IndexListView(ListView):
    template_name = "index.html"
    model = Test
    context_object_name = 'tests'


class TestTemplateView(TemplateView):
    pass


class TestsListView(ListView):
    template_name = "index.html"
    model = Test
    context_object_name = 'tests'

    def post(self, request, *args, **kwargs):
        tests = Test.objects.all().filter(name__contains=self.request.POST['find_text']) or \
            Test.objects.all().filter(description__contains=self.request.POST['find_text'])
        return render(request, self.template_name, context={'tests': tests})

    def get_queryset(self):
        return super().get_queryset()
