"""
URL configuration for Sistema_de_inventario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from .views import HomeView, ProveedoresView, MovementView, CategoriaView, legalView
from inventario import views
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('proveedores/', ProveedoresView.as_view(), name='proveedores'),
    path('movimientos/', MovementView.as_view(), name='movimientos'),
    path('categorias/', CategoriaView.as_view(), name='categoria'),
    path('graficos/', views.stock_dashboard_view, name='graficos'),

    path('productos/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('categorias/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('proveedores/create/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('stock/create/', views.StockMovementCreateView.as_view(), name='stock_create'),
    path('productos/importar/', views.product_import_csv, name='product_import'),

    path('legal/', legalView.as_view(), name='legal'),
    path('admin/', admin.site.urls),
]
