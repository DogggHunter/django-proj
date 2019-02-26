from django.urls import path, include

from . import views

app_name = 'testing_app'

urlpatterns = [
    path('test/<int:pk>/', views.TestDetailView.as_view(), name='test'),
    path('test/create/', views.TestCreateView.as_view(), name='test_create'),
    path('test/<int:pk>/update/', views.TestUpdateView.as_view(), name='test_update'),
    path('test/<int:pk>/delete/', views.TestDeleteView.as_view(), name='test_delete'),
    path('test/<int:pk>/run/', views.TestPassageDetailView.as_view(), name='test_run'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(), name='question'),
    path('question/create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('question/<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('testrun/<int:pk>/', views.TestRunDetailView.as_view(), name='testrun'),
    path('testruns/', views.TestRunsListView.as_view(), name='testruns'),
]
