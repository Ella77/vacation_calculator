# Generated by Django 2.1 on 2018-08-30 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datepick', '0009_auto_20180830_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promise',
            name='replace_day',
            field=models.IntegerField(default=0),
        ),
    ]
