# Generated by Django 4.2 on 2024-02-26 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0004_alter_alert_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='created_at',
            new_name='created',
        ),
        migrations.AlterField(
            model_name='alert',
            name='asset',
            field=models.CharField(choices=[('BTCUSDT', 'BTCUSDT'), ('ETHUSDT', 'ETHUSDT'), ('DOGEUSDT', 'DOGEUSDT')], max_length=15),
        ),
        migrations.AlterField(
            model_name='alert',
            name='triggered_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
