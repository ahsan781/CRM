# Generated by Django 4.0 on 2022-02-04 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(choices=[('Schedule video ', 'Schedule video '), ('Posted video', 'Posted video'), ('Other', 'Other')], max_length=200),
        ),
    ]