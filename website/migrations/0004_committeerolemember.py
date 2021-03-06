# Generated by Django 2.0.5 on 2018-09-01 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20180826_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitteeRoleMember',
            fields=[
                ('role_codename', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=100)),
                ('role_description', models.TextField()),
                ('member_name', models.CharField(max_length=100)),
                ('member_nickname', models.CharField(max_length=50)),
                ('member_pic_file', models.CharField(max_length=100)),
                ('member_manifesto', models.TextField()),
                ('member_email', models.EmailField(max_length=100)),
                ('member_facebook', models.URLField()),
            ],
        ),
    ]
