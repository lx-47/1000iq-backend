# Generated by Django 5.1.1 on 2024-11-11 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0033_alter_lesson_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='discount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]