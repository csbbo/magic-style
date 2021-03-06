# Generated by Django 3.0.3 on 2020-03-24 08:10

import account.models
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=64, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('old_password', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=128, null=True), default=list, size=None)),
                ('user_type', models.CharField(default='normal_user', max_length=32)),
                ('phone_number', models.CharField(max_length=11, null=True, unique=True)),
                ('email', models.TextField(null=True, unique=True)),
                ('avatar_path', models.TextField(null=True)),
                ('remark', models.TextField(null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_login_time', models.DateTimeField(null=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'user',
                'ordering': ['id'],
            },
            managers=[
                ('object', account.models.UserManager()),
            ],
        ),
    ]
