# Generated by Django 2.1.2 on 2018-10-29 18:28

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20181029_1722'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['sort_order']},
        ),
        migrations.AlterModelOptions(
            name='itemimage',
            options={'ordering': ['sort_order']},
        ),
        migrations.AlterModelOptions(
            name='itemoption',
            options={'ordering': ['paypal_option_number']},
        ),
        migrations.AlterModelOptions(
            name='optionchoice',
            options={'ordering': ['sort_order']},
        ),
        migrations.AlterModelOptions(
            name='sale',
            options={'ordering': ['start']},
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(verbose_name='item description'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=50, verbose_name='item name'),
        ),
        migrations.AlterField(
            model_name='item',
            name='paypal_button_id',
            field=models.CharField(max_length=50, verbose_name='item PayPal button ID'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='item price'),
        ),
        migrations.AlterField(
            model_name='item',
            name='sort_order',
            field=models.IntegerField(blank=True, null=True, verbose_name='item sort order'),
        ),
        migrations.AlterField(
            model_name='itemimage',
            name='image',
            field=models.ImageField(upload_to=shop.models.item_image_file_name, verbose_name='item image'),
        ),
        migrations.AlterField(
            model_name='itemimage',
            name='sort_order',
            field=models.IntegerField(blank=True, null=True, verbose_name='item image sort order'),
        ),
        migrations.AlterField(
            model_name='itemoption',
            name='auto_value',
            field=models.CharField(blank=True, choices=[('username', 'Username')], max_length=20, null=True, verbose_name='auto value type'),
        ),
        migrations.AlterField(
            model_name='itemoption',
            name='name',
            field=models.CharField(max_length=20, verbose_name='item option name'),
        ),
        migrations.AlterField(
            model_name='optionchoice',
            name='name',
            field=models.CharField(max_length=150, verbose_name='option choice display name'),
        ),
        migrations.AlterField(
            model_name='optionchoice',
            name='sort_order',
            field=models.IntegerField(blank=True, null=True, verbose_name='option choice sort order'),
        ),
        migrations.AlterField(
            model_name='optionchoice',
            name='value',
            field=models.CharField(max_length=20, verbose_name='option choice value'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='end',
            field=models.DateTimeField(verbose_name='sale end time'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='name',
            field=models.CharField(max_length=50, verbose_name='sale name'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='start',
            field=models.DateTimeField(verbose_name='sale start time'),
        ),
    ]