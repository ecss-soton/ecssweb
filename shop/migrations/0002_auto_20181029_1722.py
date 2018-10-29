# Generated by Django 2.1.2 on 2018-10-29 17:22

from django.db import migrations, models
import django.db.models.deletion
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=shop.models.item_image_file_name)),
                ('sort_order', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
        migrations.AlterField(
            model_name='optionchoice',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AddField(
            model_name='itemimage',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Item'),
        ),
    ]
