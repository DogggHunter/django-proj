# Generated by Django 2.1.5 on 2019-02-18 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testingapp', '0003_testrunanswers_created_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testrunanswers',
            name='created_on',
        ),
        migrations.AddField(
            model_name='testrun',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]