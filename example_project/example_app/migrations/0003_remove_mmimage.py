# Generated by Django 3.1.13 on 2021-12-22 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example_app', '0002_image_generic_m2m_relation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MMImage',
        ),
        migrations.AlterField(
            model_name='mmexample',
            name='images',
            field=models.ManyToManyField(blank=True, to='example_app.ImageModel'),
        ),
    ]
