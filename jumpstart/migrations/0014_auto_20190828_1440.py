# Generated by Django 2.2.1 on 2019-08-28 13:40

from django.db import migrations, models
import django.db.models.deletion
import jumpstart.models
import jumpstart.validators


class Migration(migrations.Migration):

    dependencies = [
        ('jumpstart', '0013_auto_20190827_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='fresher',
            name='is_checked_in',
            field=models.BooleanField(default=False, verbose_name='Checked In'),
        ),
        migrations.AddField(
            model_name='fresher',
            name='preferred_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='preferred Name'),
        ),
        migrations.AlterField(
            model_name='fresher',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jumpstart.Group', verbose_name='Group'),
        ),
        migrations.AlterField(
            model_name='fresher',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='fresher',
            name='username',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Username'),
        ),
        migrations.AlterField(
            model_name='helper',
            name='group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='jumpstart.Group', verbose_name='Group'),
        ),
        migrations.AlterField(
            model_name='helper',
            name='photo',
            field=models.ImageField(blank=True, upload_to=jumpstart.models.helper_photo_file_name, validators=[jumpstart.validators.validate_photo_file_extension], verbose_name='Photo'),
        ),
    ]
