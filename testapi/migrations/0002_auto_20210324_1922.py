# Generated by Django 3.1.7 on 2021-03-24 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
