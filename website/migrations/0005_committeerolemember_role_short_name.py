# Generated by Django 2.0.5 on 2018-09-02 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_committeerolemember'),
    ]

    operations = [
        migrations.AddField(
            model_name='committeerolemember',
            name='role_short_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
