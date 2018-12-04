# Generated by Django 2.1.3 on 2018-12-03 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_text', models.CharField(max_length=200)),
                ('task_start_date', models.DateTimeField(verbose_name='date start')),
                ('task_duration', models.DateTimeField(verbose_name='task duration')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_login', models.CharField(max_length=32)),
                ('user_password', models.CharField(max_length=100)),
            ],
        ),
    ]