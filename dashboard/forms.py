from django import forms
from sale.models import Product, ProductImage, Supplier, Customer, Sale

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'description', 'price', 'category', 'supplier', 'brand', 'discount', 'number']
    
    # Personalizar los widgets para agregar clases de Bootstrap
    code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código del Producto'}),
        required=True
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Producto'}),
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del Producto'}),
        required=False
    )
    brand = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca del Producto'}),
        required=False
    )
    category = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Categoría del Producto'}),
        required=True
    )
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio del Producto'}),
        required=True,
        min_value=0
    )
    discount = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Descuento en %'}),
        required=False,
        min_value=0,
        initial=0
    )
    number = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad en Inventario'}),
        required=True,
        min_value=0
    )
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    # Esto es para agregar clases de Bootstrap de manera uniforme
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in (forms.TextInput, forms.NumberInput, forms.Textarea, forms.Select):
                field.widget.attrs['class'] = 'form-control'


# Widget personalizado para manejar múltiples archivos
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True  # Permite la selección de múltiples archivos


# Campo de formulario personalizado para manejar múltiples archivos
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # Limpiar cada archivo individualmente
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):  # Si recibimos una lista de archivos
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']  # Solo el campo de la imagen

    image = MultipleFileField(
        widget=MultipleFileInput(attrs={'class': 'form-control', 'multiple': True}),
        required=False  # Permite que el campo sea opcional
    )

    def save_images(self, product):
        """
        Método personalizado para guardar las imágenes en la base de datos.
        :param product: Instancia del producto al que se asociarán las imágenes.
        """
        images = self.files.getlist('image')  # Cambiado a self.files para obtener la lista de imágenes
        if images:
            for image_file in images:
                ProductImage.objects.create(product=product, image=image_file)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'is_active', 'avatar']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'customer', 'price', 'status', 'reference']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),  # Añadí el cierre correcto aquí
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_reference(self):
        reference = self.cleaned_data.get('reference')
        if not self.instance.pk and Sale.objects.filter(reference=reference).exists():
            raise forms.ValidationError("Esta referencia ya existe.")
        return reference