# Generated by Django 5.0.14 on 2025-06-07 05:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botbot', '0007_alter_gamuser_user'),
        ('letters', '0006_alter_summaryletter_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='LetterArchive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter_id', models.CharField(max_length=10)),
                ('sent_time', models.CharField(max_length=300)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='botbot.gamuser')),
            ],
        ),
    ]
