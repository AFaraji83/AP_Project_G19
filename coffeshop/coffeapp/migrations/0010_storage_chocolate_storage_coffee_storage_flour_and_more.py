# Generated by Django 5.0.6 on 2024-07-03 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffeapp', '0008_alter_storage_options_remove_storage_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='chocolate',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='storage',
            name='coffee',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='storage',
            name='flour',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='storage',
            name='sugar',
            field=models.IntegerField(default=0),
        ),
    ]
