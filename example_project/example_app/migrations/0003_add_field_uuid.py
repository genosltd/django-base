# Generated by Django 3.1.13 on 2021-09-08 12:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('example_app', '0002_historicalexamplemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='examplemodel',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='historicalexamplemodel',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]