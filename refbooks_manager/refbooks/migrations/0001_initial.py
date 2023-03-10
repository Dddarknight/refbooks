# Generated by Django 4.1.4 on 2022-12-21 08:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RefBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'refbook',
                'verbose_name_plural': 'refbooks',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=50)),
                ('start_date', models.DateField(default=django.utils.timezone.now, unique=True)),
                ('refbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='refbooks.refbook')),
            ],
            options={
                'verbose_name': 'version',
                'verbose_name_plural': 'versions',
                'ordering': ['version'],
                'unique_together': {('refbook', 'start_date'), ('refbook', 'version')},
            },
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=300)),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='refbooks.version')),
            ],
            options={
                'verbose_name': 'element',
                'verbose_name_plural': 'elements',
                'ordering': ['code'],
                'unique_together': {('version', 'code')},
            },
        ),
    ]
