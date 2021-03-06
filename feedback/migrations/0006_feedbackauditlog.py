# Generated by Django 2.0.5 on 2018-07-28 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_auto_20180727_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackAuditLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('respond', 'responded'), ('edit', 'edited'), ('delet', 'deleted')], max_length=20)),
                ('user', models.CharField(max_length=150)),
                ('feedback', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='feedback.Feedback')),
            ],
        ),
    ]
