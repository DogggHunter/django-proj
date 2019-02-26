from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    questions = models.ManyToManyField('Question')
    notes = GenericRelation('NoteItem')

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
    notes = GenericRelation('NoteItem')

    class Meta:
        verbose_name = 'testrun'


class TestRunAnswers(models.Model):
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)


class Note(models.Model):
    description = models.CharField(max_length=200)


class NoteItem(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.note.description
