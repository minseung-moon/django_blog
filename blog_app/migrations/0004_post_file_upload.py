# Generated by Django 3.1.7 on 2021-04-06 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0003_post_head_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='file_upload',
            field=models.FileField(blank=True, upload_to='blog_app/files/%Y/%m/%d/'),
        ),
    ]
