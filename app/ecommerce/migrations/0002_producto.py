# Generated by Django 3.2.4 on 2021-06-21 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150, unique=True, verbose_name='Titulo')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='producto/%Y/%m/%d', verbose_name='Imagen')),
                ('descripcion', models.CharField(max_length=250, verbose_name='Descripcion')),
                ('precio', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio de venta')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.categoria', verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['id'],
            },
        ),
    ]
