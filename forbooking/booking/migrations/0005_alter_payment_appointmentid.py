# Generated by Django 4.0.6 on 2022-09-30 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_alter_payment_appointmentid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='appointmentid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.slot'),
        ),
    ]
