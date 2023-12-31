# Generated by Django 4.2.6 on 2023-11-27 05:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_task_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_member',
            field=models.ManyToManyField(related_name='user_team_member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='TeamMember',
        ),
    ]
