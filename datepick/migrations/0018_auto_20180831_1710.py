# Generated by Django 2.1 on 2018-08-31 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datepick', '0017_promise_regi_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promise',
            name='regi_status',
            field=models.BooleanField(default=True),
        ),
    ]