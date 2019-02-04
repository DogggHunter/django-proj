from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    questions = models.ManyToManyField('Question', through='QuestionTest')

    def __str__(self):
        return self.name


class Question(models.Model):
    description = models.CharField(max_length=350)


class QuestionTest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class TestRun(models.Model):
    pass
