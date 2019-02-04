from django.contrib import admin
from .models import Test, Question


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

