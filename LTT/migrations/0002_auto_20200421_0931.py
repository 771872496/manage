# Generated by Django 2.0.1 on 2020-04-21 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LTT', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ltt',
            name='log',
            field=models.FileField(blank=True, null=True, upload_to='l_log'),
        ),
    ]
