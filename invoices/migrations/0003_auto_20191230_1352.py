# Generated by Django 3.0 on 2019-12-30 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_auto_20191217_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='address',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='amount_paid',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='cumulative_paid',
        ),
        migrations.AddField(
            model_name='invoice',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invoice',
            name='total_net_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_type',
            field=models.CharField(choices=[('CC', 'CREDIT CARD'), ('CA', 'CASH'), ('BT', 'BANK TRANSFER'), ('DC', 'DEBIT CARD'), ('NA', 'NA')], default='NA', max_length=2),
        ),
    ]
