# Generated by Django 5.1.1 on 2024-11-07 06:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0016_alter_question_assessment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='is_correct',
        ),
        migrations.AddField(
            model_name='question',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='answer', to='lms.choice'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson', to='lms.section'),
        ),
    ]
