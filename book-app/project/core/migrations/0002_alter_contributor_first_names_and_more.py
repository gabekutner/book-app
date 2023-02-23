# Generated by Django 4.1.3 on 2023-02-22 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='first_names',
            field=models.CharField(help_text="The contributor's first name or names.", max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='last_names',
            field=models.CharField(help_text="The contributor's last name or names.", max_length=50, unique=True),
        ),
    ]
