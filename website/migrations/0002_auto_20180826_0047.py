# Generated by Django 2.0.5 on 2018-08-25 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='society',
            name='twitter',
            field=models.CharField(max_length=100),
        ),
    ]