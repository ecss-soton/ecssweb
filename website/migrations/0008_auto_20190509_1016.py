# Generated by Django 2.1.2 on 2019-05-09 09:16

from django.db import migrations, models
import website.models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20181006_2157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='committeerolemember',
            name='member_pic_file',
        ),
        migrations.AddField(
            model_name='committeerolemember',
            name='member_image',
            field=models.ImageField(default='', upload_to=website.models.committee_member_image_file_name),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='committeerolemember',
            name='member_facebook',
            field=models.URLField(blank=True),
        ),
    ]
