# Generated by Django 4.1.5 on 2023-02-05 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_card_last_use_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='last_use_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
