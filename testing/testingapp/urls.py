from django.urls import path

from . import views

app_name = 'testingapp'

urlpatterns = [
    path('<int:test_id>/', views.TestTemplateView.as_view(), name='test'),
    path('search/', views.TestsListView.as_view(), name='find_tests')
]
