# Generated by Django 2.0.5 on 2018-09-23 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jumpstart', '0008_citychallengescoreauditlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='games_challenge_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='sports_challenge_score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
