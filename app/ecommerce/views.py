from django.db.models import Sum
import json

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.ecommerce.forms import CategoriaForm, ProductoForm
from app.ecommerce.models import Categoria, Producto, Carrito


# Vista HOME
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Jaguarete KAA S.A.'
        context['title'] = 'Jaguarete KAA S.A.'
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


# Vistas de Categoria
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria/list.html'
    ordering = ['descripcion']

    # @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


class ProductosCategoriaListView(ListView):
    template_name = 'producto/list.html'

    def get_queryset(self):
        self.categoria = get_object_or_404(Categoria, id=self.kwargs['pk'])
        return Producto.objects.filter(categoria=self.categoria)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos de la Categoría'
        context['create_url'] = reverse_lazy('ecommerce:producto_create')
        context['list_url'] = reverse_lazy('ecommerce:producto_list')
        context['entity'] = 'Productos'
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        context['categoria'] = self.categoria
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria/create.html'
    success_url = reverse_lazy('ecommerce:categoria_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria/create.html'
    success_url = reverse_lazy('ecommerce:categoria_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

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
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        context['action'] = 'edit'
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'categoria/delete.html'
    success_url = reverse_lazy('ecommerce:categoria_list')
    url_redirect = success_url

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
        context['title'] = 'Eliminar una Categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = self.success_url
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


# Vistas de Producto
class ProductoListView(ListView):
    model = Producto
    template_name = 'producto/list.html'

    # template_name = 'producto/listProdCarrito.html'

    # @method_decorator(csrf_exempt)
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
        context['create_url'] = reverse_lazy('ecommerce:producto_create')
        context['list_url'] = reverse_lazy('ecommerce:producto_list')
        context['entity'] = 'Productos'
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/create.html'
    success_url = reverse_lazy('ecommerce:producto_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/create.html'
    success_url = reverse_lazy('ecommerce:producto_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

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
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'producto/delete.html'
    success_url = reverse_lazy('ecommerce:producto_list')
    url_redirect = success_url

    # @method_decorator(login_required)
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
        context['title'] = 'Eliminar un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


# Vistas de Producto Usuario Comun
class ProductoUsuarioListView(ListView):
    model = Producto
    template_name = 'producto/listProdCarrito.html'

    # @method_decorator(csrf_exempt)
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
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


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
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        context['producto'] = self.producto
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


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

def deleteCart(request):
    data = json.loads(request.body)
    # Obtenemos el producto y la accion
    carritoId = data['carritoId']
    action = data['action']
    # Obtenemos el usuario actual
    carrito = request.id
    if action == 'delete':
        carrito = Carrito.objects.delete(carrito=carrito)
        carrito.save()
    return JsonResponse('Producto eliminado del carrito', safe=False)


class CarritoListView(ListView):
    model = Carrito
    template_name = 'carrito/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        # Filtrar el Listview para ver con el Usuario activo
        return qs.filter(usuario__id=self.request.user.id)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                user = self.request.user.id
                print(user)
                data = []
                # for i in Carrito.objects.all():
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
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        # Ver si el usuario esta autenticado
        try:
            context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        except Exception as e:
            pass
        return context


class CarritoDeleteView(DeleteView):
    model = Carrito
    template_name = 'carrito/delete.html'
    success_url = reverse_lazy('ecommerce:carrito_list')
    url_redirect = success_url

    # def get_queryset(self):
    #     self.producto = get_object_or_404(Carrito, id=self.kwargs['pk'])
    #     print(self.producto.producto.pk)
    #     return Producto.objects.filter(id=self.producto.producto.pk)

    # @method_decorator(login_required)
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
        context['categorias'] = Categoria.objects.all()
        context['productos'] = Producto.objects.all()
        context['carrito'] = Carrito.objects.filter(usuario=self.request.user).count()
        return context
