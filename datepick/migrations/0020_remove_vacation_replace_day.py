# Generated by Django 2.1 on 2018-09-03 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datepick', '0019_auto_20180903_1812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacation',
            name='replace_day',
        ),
    ]
