# Generated by Django 2.0.5 on 2018-09-12 14:56

from django.db import migrations
import ecsswebauth.models


class Migration(migrations.Migration):

    dependencies = [
        ('ecsswebauth', '0002_auto_20180726_2208'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='ecsswebusergroup',
            managers=[
                ('objects', ecsswebauth.models.EcsswebUserGroupManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='samluser',
            managers=[
                ('objects', ecsswebauth.models.SamlUserManager()),
            ],
        ),
    ]
