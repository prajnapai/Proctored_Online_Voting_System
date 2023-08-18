# Generated by Django 4.1.7 on 2023-05-04 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('eid', models.IntegerField(default=None, primary_key=True, serialize=False)),
                ('election_title', models.CharField(max_length=50)),
                ('election_date', models.DateField()),
                ('election_description', models.TextField()),
                ('election_status', models.TextField()),
            ],
        ),
    ]
