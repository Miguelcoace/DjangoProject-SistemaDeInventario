from .models import Product, Category, Supplier, StockMovement
from django.views.generic import CreateView
from .forms import CategoryCreateForm, SupplierCreateForm, ProductCreateForm, StockMovementCreateForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CSVImportForm
import csv
from django.db.models import Sum
import json

# Create your views here.
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = "_general/_category_form.html"
    success_url = reverse_lazy('categoria')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Categoría creada correctamente")
        return super(CategoryCreateView, self).form_valid(form)


class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierCreateForm
    template_name = "_general/_supplier_form.html"
    success_url = reverse_lazy('proveedores')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Proveedor creado correctamente")
        return super(SupplierCreateView, self).form_valid(form)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = "_general/_product_form.html"
    success_url = reverse_lazy('home')

    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Producto creado correctamente")
        return super(ProductCreateView, self).form_valid(form)

class StockMovementCreateView(CreateView):
    model = StockMovement
    form_class = StockMovementCreateForm
    template_name = "_general/_stock_form.html"
    success_url = reverse_lazy('movimientos')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Movimiento creado correctamente")
        return super(StockMovementCreateView, self).form_valid(form)


def product_import_csv(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            # Decodificar el archivo CSV
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            
            next(reader) # Saltar la cabecera 
            
            for row in reader:
                if len(row) < 6:
                    continue
                sku, name, description, price, stock, min_stock, category_name, supplier_name = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]                
                # Obtener o crear categoría y proveedor para evitar errores
                category, _ = Category.objects.get_or_create(name=category_name.strip())
                supplier, _ = Supplier.objects.get_or_create(name=supplier_name.strip())
                
                # Crear o actualizar el producto basado en el SKU
                Product.objects.update_or_create(
                    sku=sku.strip(),
                    defaults={
                        'name': name.strip(),
                        'description': description.strip(),
                        'price': float(price),
                        'stock': int(stock),
                        'min_stock': int(min_stock),
                        'category': category,
                        'supplier': supplier
                    }
                )
            return redirect('home') # Redirige a la lista de productos
    else:
        form = CSVImportForm()
        
    return render(request, '_general/_import_csv.html', {'form': form})



def stock_dashboard_view(request):
    # 1. Agrupar la cantidad total por tipo de movimiento ('IN' y 'OUT')
    movements_summary = StockMovement.objects.values('movement_type').annotate(total_quantity=Sum('quantity'))
    
    in_total = 0
    out_total = 0
    for item in movements_summary:
        if item['movement_type'] == 'IN':
            in_total = item['total_quantity']
        elif item['movement_type'] == 'OUT':
            out_total = item['total_quantity']

    # 2. Obtener productos y sus niveles de stock actual
    products = Product.objects.all().order_by('-stock')[:10] # Top 10 productos con más stock
    product_names = [p.name for p in products]
    product_stocks = [p.stock for p in products]

    context = {
        'in_total': in_total,
        'out_total': out_total,
        'product_names': json.dumps(product_names), # Convertimos a JSON para pasarlo a JS
        'product_stocks': json.dumps(product_stocks),
    }
    
    return render(request, '_general/_stock_dashboard.html', context)