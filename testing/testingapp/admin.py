from django.contrib import admin
from .models import Test, Question, TestRun


@admin.register(Test, Question, TestRun)
class TestAdmin(admin.ModelAdmin):
    pass

