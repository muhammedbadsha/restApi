# Generated by Django 4.2.2 on 2023-06-25 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0003_alter_user_managers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
