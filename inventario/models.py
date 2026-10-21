from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=150, verbose_name="Proveedor")
    contact = models.CharField(max_length=100, blank=True, null=True, verbose_name="Contacto")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, null=True, verbose_name="Correo")

    def __str__(self):
        return self.name
    

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True, verbose_name="Código SKU")
    name = models.CharField(max_length=150, verbose_name="Nombre")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    stock = models.IntegerField(default=0, verbose_name="Stock Actual")
    min_stock = models.IntegerField(default=5, verbose_name="Stock Mínimo")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products", verbose_name="Categoría")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name="products", verbose_name="Proveedor")

    @property
    def is_low_stock(self):
        """Alerta de stock mínimo"""
        return self.stock <= self.min_stock

    def __str__(self):
        return f"{self.sku} - {self.name} (Stock: {self.stock})"


class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ('IN', 'Entrada'),
        ('OUT', 'Salida'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements', verbose_name="Producto")
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES, verbose_name="Tipo de Movimiento")
    quantity = models.IntegerField(verbose_name="Cantidad")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    notes = models.TextField(blank=True, null=True, verbose_name="Notas / Motivo")

    def clean(self):
        # Validar que no se saque mas stock del que hay
        if self.movement_type == 'OUT' and self.pk is None:
            if self.product.stock < self.quantity:
                raise ValidationError(f"Stock insuficiente. Stock actual: {self.product.stock}")

    def save(self, *args, **kwargs):
        self.full_clean()
        # Actualizar stock automáticamente al registrar el movimiento por primera vez
        if self.pk is None:
            if self.movement_type == 'IN':
                self.product.stock += self.quantity
            elif self.movement_type == 'OUT':
                self.product.stock -= self.quantity
            self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_movement_type_display()} de {self.quantity} - {self.product.name}"