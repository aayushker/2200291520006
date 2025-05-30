# Generated by Django 4.2.20 on 2025-05-09 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('last_updated_at', models.DateTimeField()),
                ('retrieved_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-last_updated_at'],
                'indexes': [models.Index(fields=['ticker', 'last_updated_at'], name='stocks_stoc_ticker_15ea25_idx')],
            },
        ),
    ]
