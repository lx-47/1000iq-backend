# Generated by Django 5.1.1 on 2024-11-05 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.CharField(max_length=255, null=True),
        ),
    ]