# Generated by Django 2.0.5 on 2018-09-25 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jumpstart', '0010_scavengerhunt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Group Name'),
        ),
    ]
