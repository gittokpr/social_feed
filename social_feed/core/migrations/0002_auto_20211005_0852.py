# Generated by Django 3.2.7 on 2021-10-05 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='postDescription',
            field=models.TextField(max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='postImage',
            field=models.TextField(max_length=5000, null=True),
        ),
    ]
