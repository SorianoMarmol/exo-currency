# Generated by Django 2.0.13 on 2019-07-24 09:41

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(db_index=True, max_length=20)),
                ('symbol', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CurrencyExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valuation_date', models.DateField(db_index=True)),
                ('rate_value', models.DecimalField(db_index=True, decimal_places=6, max_digits=18)),
                ('exchanged_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inversed_exchanges', to='exchange_rates.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('adapter', models.CharField(choices=[('FIXER', 'FIXER.IO'), ('MOCK', 'MOCK')], max_length=2, unique=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='exchange_rates.Provider', verbose_name='parent')),
            ],
            options={
                'ordering': ('tree_id', 'lft'),
                'abstract': False,
                'verbose_name_plural': 'Providers',
            },
            managers=[
                ('tree', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='currencyexchangerate',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exchange_rates.Provider'),
        ),
        migrations.AddField(
            model_name='currencyexchangerate',
            name='source_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchanges', to='exchange_rates.Currency'),
        ),
        migrations.AlterUniqueTogether(
            name='provider',
            unique_together={('parent', 'name')},
        ),
    ]
