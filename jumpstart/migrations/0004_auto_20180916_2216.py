# Generated by Django 2.0.5 on 2018-09-16 21:16

from django.db import migrations, models
import jumpstart.validators


class Migration(migrations.Migration):

    dependencies = [
        ('jumpstart', '0003_auto_20180916_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helper',
            name='photo',
            field=models.ImageField(upload_to='jumpstart2018/helpers/', validators=[jumpstart.validators.validate_photo_file_extension]),
        ),
    ]
