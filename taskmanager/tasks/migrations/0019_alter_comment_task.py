# Generated by Django 4.2.2 on 2023-06-20 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0018_alter_comment_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_comments', to='tasks.task'),
        ),
    ]
