# Generated by Django 2.1 on 2018-08-21 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datepick', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promise',
            name='status',
            field=models.IntegerField(choices=[(1, '오전 반차'), (2, '오후 반차')], default=0),
        ),
        migrations.AlterField(
            model_name='promise',
            name='end',
            field=models.DateField(default=models.DateField()),
        ),
    ]