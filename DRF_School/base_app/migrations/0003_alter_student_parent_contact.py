# Generated by Django 3.2.19 on 2023-05-09 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0002_auto_20230509_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='parent_contact',
            field=models.IntegerField(blank=True, max_length=15, null=True),
        ),
    ]