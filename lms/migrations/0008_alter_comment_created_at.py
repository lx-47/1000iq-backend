# Generated by Django 5.1.1 on 2024-11-05 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0007_tutor_first_name_tutor_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
