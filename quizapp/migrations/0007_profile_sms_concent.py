# Generated by Django 2.2.2 on 2019-07-11 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0006_profile_ontra_contact_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sms_concent',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
