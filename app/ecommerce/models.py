from django.contrib.auth.models import User
from django.db import models

from django.forms import model_to_dict

# Clase Categorias
from app.config.settings import MEDIA_URL


class Categoria(models.Model):
    descripcion = models.CharField(max_length=150, verbose_name='Descripcion', unique=True)

    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    #Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(Categoria, self).save(force_insert, force_update)

#Clase Producto
class Producto(models.Model):
    titulo = models.CharField(max_length=150, verbose_name='Titulo', unique=True)
    imagen = models.ImageField(upload_to='productos/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen', default='empty.png')
    descripcion = models.CharField(max_length=250, verbose_name='Descripcion')
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría')

    def __str__(self):
        return self.titulo

    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        item['imagen'] = self.get_image()
        item['precio'] = format(self.precio, '.2f')
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(MEDIA_URL, 'empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

    # Para convertir a MAYUSCULA
    def save(self, force_insert=False, force_update=False):
        self.titulo = self.titulo.upper()
        self.descripcion = self.descripcion.upper()
        super(Producto, self).save(force_insert, force_update)


# Clase Carrito
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.usuario.username

    def toJSON(self):
        item = model_to_dict(self)
        item['usuario'] = self.usuario.toJSON()
        item['producto'] = self.producto.toJSON()
        item['total'] = format(self.total, '.2f')
        return item

    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
        ordering = ['id']