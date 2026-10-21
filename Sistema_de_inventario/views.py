from django.views.generic import TemplateView
from inventario.models import Product, Category, Supplier, StockMovement



class HomeView(TemplateView):
    template_name = "_general/_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_products = Product.objects.all().order_by('name')

        context['all_products'] = all_products

        return context
        


class ProveedoresView(TemplateView):
    template_name = "_general/_proveedores.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_suppliers = Supplier.objects.all().order_by('name')

        context['all_suppliers'] = all_suppliers

        return context


class MovementView(TemplateView):
    template_name = "_general/_movements.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_movements = StockMovement.objects.all().order_by('date')

        context['all_movements'] = all_movements

        return context


class CategoriaView(TemplateView):
    template_name = "_general/_categorias.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_categories = Category.objects.all().order_by('name')

        context['all_categories'] = all_categories

        return context


class legalView(TemplateView):
    template_name = '_general/_legal.html'