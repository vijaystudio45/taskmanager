# Generated by Django 4.2.6 on 2023-11-23 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_remove_task_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmember',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_task', to='tasks.task'),
        ),
    ]
