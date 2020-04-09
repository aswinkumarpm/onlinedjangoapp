# Generated by Django 3.0.5 on 2020-04-08 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0003_diary_is_public'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('full_name', models.CharField(max_length=100, null=True)),
                ('message', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]