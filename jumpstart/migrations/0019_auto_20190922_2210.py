# Generated by Django 2.2.1 on 2019-09-22 21:10

from django.db import migrations, models
import django.db.models.deletion
import jumpstart.models
import jumpstart.validators


class Migration(migrations.Migration):

    dependencies = [
        ('jumpstart', '0018_auto_20190922_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='HintRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jumpstart.Group')),
            ],
        ),
        migrations.CreateModel(
            name='ScavengerHuntSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=jumpstart.models.scavenger_hunt_submission_photo_file_name, validators=[jumpstart.validators.validate_photo_file_extension], verbose_name='Scavenger Hunt Photo')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jumpstart.Group')),
            ],
        ),
        migrations.CreateModel(
            name='ScavengerHuntTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('hint', models.TextField(blank=True, null=True)),
                ('points', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='charityshopchallengesubmission',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='ScavengerHunt',
        ),
        migrations.AddField(
            model_name='scavengerhuntsubmission',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jumpstart.ScavengerHuntTask'),
        ),
        migrations.AddField(
            model_name='hintrecord',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jumpstart.ScavengerHuntTask'),
        ),
    ]
