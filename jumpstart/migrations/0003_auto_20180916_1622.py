# Generated by Django 2.0.5 on 2018-09-16 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jumpstart', '0002_helper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helper',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
