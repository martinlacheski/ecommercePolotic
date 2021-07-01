from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import json

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.ecommerce.forms import CategoriaForm, ProductoForm
from app.ecommerce.models import Categoria, Producto, Carrito


# Vista Inicio
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    #Metodo para buscar productos en la barra de busqueda
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'autocomplete':
                data = []
                for i in Producto.objects.filter(titulo__icontains=request.POST['term'])[0:10]:
                    item = {}
                    item['id'] = i.id
                    item['value'] = i.titulo
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Jaguarete KAA S.A.'
        context['title'] = 'Jaguarete KAA S.A.'
        #Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        context['principales'] = Producto.objects.all().order_by("-id")[:3]
        context['secundarios'] = Producto.objects.all().order_by("-id")[3:10]
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context

# Vista Contacto
class ContactoView(TemplateView):
    template_name = 'contacto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Jaguarete KAA S.A.'
        context['title'] = 'Jaguarete KAA S.A.'
        #Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


# Vista Contacto
class AcercaView(TemplateView):
    template_name = 'acerca.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Jaguarete KAA S.A.'
        context['title'] = 'Jaguarete KAA S.A.'
        #Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context

# Vistas de Categoria

#Vista Listar Categorias
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria/list.html'
    ordering = ['descripcion']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('ecommerce:dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Categoria.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Categorías'
        context['create_url'] = reverse_lazy('ecommerce:categoria_create')
        context['list_url'] = reverse_lazy('ecommerce:categoria_list')
        context['entity'] = 'Categorias'
        # Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


#Vista Lista de Productos de UNA Categoria
class ProductosCategoriaListView(ListView):
    template_name = 'producto/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('ecommerce:dashboard')

    def get_queryset(self):
        self.categoria = get_object_or_404(Categoria, id=self.kwargs['pk'])
        return Producto.objects.filter(categoria=self.categoria)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos de la Categoría'
        context['create_url'] = reverse_lazy('ecommerce:producto_create')
        context['list_url'] = reverse_lazy('ecommerce:producto_list')
        context['entity'] = 'Productos'
        # Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Se agrega al context_data para llamar a los productos que corresponden a la categoria
        context['categoria'] = self.categoria
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


#Vista de Crear Categoria
class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria/create.html'
    success_url = reverse_lazy('ecommerce:categoria_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('ecommerce:dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
                return HttpResponseRedirect(self.success_url)
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear una Categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        # Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


#Vista Actualizar Categoria
class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria/create.html'
    success_url = reverse_lazy('ecommerce:categoria_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.object = self.get_object()
            return super().dispatch(request, *args, **kwargs)
        return redirect('ecommerce:dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
                return HttpResponseRedirect(self.success_url)
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar una Categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = self.success_url
        # Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        context['action'] = 'edit'
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


#Vista Borrar Categoria
class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'categoria/delete.html'
    success_url = reverse_lazy('ecommerce:categoria_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.object = self.get_object()
            return super().dispatch(request, *args, **kwargs)
        return redirect('ecommerce:dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar una Categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = self.success_url
        # Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


# Vistas de Producto

#Vista Listar Productos
class ProductoListView(ListView):
    model = Producto
    template_name = 'producto/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('ecommerce:dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Producto.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('ecommerce:producto_create')
        context['list_url'] = reverse_lazy('ecommerce:producto_list')
        context['entity'] = 'Productos'
        # Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


#Vista Crear Producto
class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/create.html'
    success_url = reverse_lazy('ecommerce:producto_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('ecommerce:dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
                return HttpResponseRedirect(self.success_url)
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        # Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


#Vista Actualizar Producto
class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/create.html'
    success_url = reverse_lazy('ecommerce:producto_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.object = self.get_object()
            return super().dispatch(request, *args, **kwargs)
        return redirect('ecommerce:dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
                return HttpResponseRedirect(self.success_url)
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        # Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


#Vista Borrar Producto
class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'producto/delete.html'
    success_url = reverse_lazy('ecommerce:producto_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.object = self.get_object()
            return super().dispatch(request, *args, **kwargs)
        return redirect('ecommerce:dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        # Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


# Vistas de Producto Usuario Comun

#Vista Listado de Productos
class ProductoUsuarioListView(ListView):
    model = Producto
    template_name = 'producto/listProdCarrito.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Producto.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['list_url'] = reverse_lazy('ecommerce:producto_usuario_list')
        context['entity'] = 'Productos'
        # Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


#Vista Ver UN Producto
class ProductoView(ListView):
    template_name = 'producto/producto.html'

    def get_queryset(self):
        self.producto = get_object_or_404(Producto, id=self.kwargs['pk'])
        return Producto.objects.filter(id=self.producto.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ver Producto'
        context['list_url'] = reverse_lazy('ecommerce:producto_usuario_list')
        context['entity'] = 'Producto'
        # Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Se agrega al context_data para ver los datos del producto individual
        context['producto'] = self.producto
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


#Vista de producto desde el dashboard
class ProductoDashboardView(ListView):
    template_name = 'producto/productoDashboard.html'

    def get_queryset(self):
        self.producto = get_object_or_404(Producto, id=self.kwargs['pk'])
        return Producto.objects.filter(id=self.producto.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ver Producto'
        context['list_url'] = reverse_lazy('ecommerce:producto_usuario_list')
        context['entity'] = 'Producto'
        # Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        context['producto'] = self.producto
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


# Funciones y Vistas de Carrito

#Funcion Agregar un producto al carrito
def addCart(request):
    data = json.loads(request.body)
    # Obtenemos el producto y la accion
    productId = data['productId']
    action = data['action']
    # Obtenemos el usuario actual
    usuario = request.user
    producto = Producto.objects.get(id=productId)
    if action == 'add':
        carrito = Carrito.objects.create(usuario=usuario, producto=producto, total=producto.precio)
        carrito.save()
    return JsonResponse('Producto agregado al carrito', safe=False)


#Listar los productos del Carrito
class CarritoListView(ListView):
    model = Carrito
    template_name = 'carrito/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        # Filtrar el Listview para ver con el Usuario activo
        return qs.filter(usuario__id=self.request.user.id)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                user = self.request.user.id
                data = []
                for i in Carrito.objects.filter(usuario__id=user):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Carrito'
        context['list_url'] = reverse_lazy('ecommerce:carrito_list')
        context['entity'] = 'Carrito'
        # Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context

#Eliminar productos del Carrito
class CarritoDeleteView(DeleteView):
    model = Carrito
    template_name = 'carrito/delete.html'
    success_url = reverse_lazy('ecommerce:carrito_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar un Producto del Carrito'
        context['entity'] = 'Carrito'
        context['list_url'] = self.success_url
        # Se agrega al context_data para llamar desde el header y dashboard para completar
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Se agrega al context_data para filtrar los productos que corresponden al usuario logueado
        context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        return context


#Comprar Carrito
def purchaseCart(request):
    data = json.loads(request.body)
    print("aca llega")
    # Obtenemos la accion
    action = data['action']
    # Obtenemos el usuario actual
    usuario = request.user
    if action == 'add':
        carrito = Carrito.objects.filter(usuario=usuario).delete()
    return JsonResponse('Carrito Comprado', safe=False)
