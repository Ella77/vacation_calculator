# Generated by Django 2.1 on 2018-08-31 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datepick', '0015_auto_20180831_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promise',
            name='reason',
            field=models.CharField(choices=[('매직데이', '매직데이'), ('경사', '경사'), ('조사', '조사')], max_length=100),
        ),
    ]
