# Generated by Django 5.1.3 on 2024-11-08 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_is_staff_user_is_superuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbankaccount',
            old_name='account_no',
            new_name='account_number',
        ),
    ]
