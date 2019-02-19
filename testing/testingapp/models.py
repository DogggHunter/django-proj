from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    questions = models.ManyToManyField('Question')

    def __str__(self):
        return self.name


class Question(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description


class TestRun(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, through='TestRunAnswers', through_fields=('test_run', 'question'))
    created_on = models.DateTimeField(auto_now_add=True, null=True)


class TestRunAnswers(models.Model):
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
