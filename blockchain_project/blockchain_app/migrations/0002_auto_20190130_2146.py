# Generated by Django 2.1.2 on 2019-01-30 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='timestamp',
            field=models.FloatField(default=1548884794.591239),
        ),
        migrations.AlterField(
            model_name='node',
            name='timestamp',
            field=models.FloatField(default=1548884794.593045),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.FloatField(default=1548884794.592062),
        ),
    ]
