# Generated by Django 4.1.2 on 2022-10-28 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_produto', models.DecimalField(decimal_places=2, default=0.0, help_text='Valor original do produto', max_digits=10)),
                ('desconto', models.DecimalField(decimal_places=2, default=0.0, help_text='Desconto do produto', max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, help_text='Valor com desconto', max_digits=100)),
                ('taxa_envio_outros', models.DecimalField(decimal_places=2, default=0.0, help_text='Taxa de enviou, adesão ou manutenção', max_digits=10)),
                ('valor_total', models.DecimalField(decimal_places=2, default=0.0, help_text='Valor total a ser pago', max_digits=10)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('data_hora', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('produto', models.ManyToManyField(blank=True, to='products.products')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cart',
                'db_table': 'cart',
                'ordering': ('-atualizado_em',),
            },
        ),
    ]