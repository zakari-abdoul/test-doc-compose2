# Generated by Django 3.1.5 on 2021-02-15 12:28

from django.db import migrations, models
import uploadFile.models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadFile', '0005_auto_20210211_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='files',
            field=models.FileField(upload_to=uploadFile.models.generate_filename),
        ),
    ]
