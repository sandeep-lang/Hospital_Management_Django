# Generated by Django 4.0.6 on 2022-09-30 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_remove_slot_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='appointmentid',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
