# Generated by Django 3.0 on 2019-12-30 13:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0003_auto_20191230_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='paid_on',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Paid on'),
            preserve_default=False,
        ),
    ]
