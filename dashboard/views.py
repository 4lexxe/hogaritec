from django.shortcuts import render, redirect
from django.db.models import Sum
from .forms import ProductForm, CustomerForm
from sale.models import Product, Customer,Sale, Subscriber, Supplier, ProductImage, Order, OrderItem, Payment
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from decimal import Decimal
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone

@login_required
def dashboard_view(request):
    # Verifica si el usuario es un superusuario
    if not request.user.is_superuser:
        raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

    # Total de productos
    total_products = Product.objects.count()

    # Ventas del mes
    current_month = now().month
    current_year = now().year
    sales_this_month = Sale.objects.filter(date__year=current_year, date__month=current_month)
    total_sales = sales_this_month.aggregate(Sum('price'))['price__sum'] or 0  # Evitar None si no hay ventas

# Calcular el total de ventas del mes actual desde las órdenes
    current_month = timezone.now().month
    current_year = timezone.now().year
    total_sales_orders = Order.objects.filter(
        date__year=current_year, 
        date__month=current_month
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Nuevas ventas (todas las ventas para mostrar en la tabla)
    sales = Sale.objects.all().order_by('-date')

    # Nuevos clientes del mes
    new_customers = Customer.objects.filter(date_joined__year=current_year, date_joined__month=current_month).count()

    # Pedidos pendientes
    pending_orders_count = Sale.objects.filter(status='pending').count()

    # Limitar productos
    products = Product.objects.prefetch_related('images', 'supplier').order_by('-created')[:5]

    # Obtener los últimos suscriptores
    subscribers = Subscriber.objects.order_by('-date_subscribed')[:5]

    # Obtener los últimos clientes
    customers = Customer.objects.order_by('-date_joined')[:5]

    # Obtener los últimos proveedores
    suppliers = Supplier.objects.order_by('-id')[:5]
    suppliersAll = Supplier.objects.all()

    # Obtener las últimas 5 órdenes
    latest_orders = Order.objects.select_related('customer').order_by('-date')[:5]

    return render(request, 'dashboard/dashboard.html', {
        'total_products': total_products,
        'total_sales': total_sales,
        'new_customers': new_customers,
        'products': products,
        'subscribers': subscribers,
        'customers': customers,
        'suppliers': suppliers,
        'suppliersAll': suppliersAll,
        'sales': sales,
        'pending_orders_count': pending_orders_count,
        'latest_orders': latest_orders,  # Añadimos las últimas órdenes al contexto
        'total_sales_orders': total_sales_orders
    })

@login_required
def products_dashboard_view(request):
  # Verifica si el usuario es un superusuario
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  # Obtener todos los productos
  products = Product.objects.all()  # Obtiene todos los productos

  return render(request, 'dashboard/products.html', {
    'products': products,
  })

@login_required
def subscribers_dashboard_view(request):
  # Verifica si el usuario es un superusuario
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  # Obtener todos los suscriptores
  subscribers = Subscriber.objects.all()

  return render(request, 'dashboard/subscribers.html', {
    'subscribers': subscribers,
  })

@login_required
def sales_dashboard_view(request):
  # Verifica si el usuario es un superusuario
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  # Obtener todas las ventas
  sales = Sale.objects.all().order_by('-date')

  return render(request, 'dashboard/sales.html', {
    'sales': sales,
  })

@login_required
def customers_dashboard_view(request):
  # Verifica si el usuario es un superusuario
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  # Obtener todos los clientes
  customers = Customer.objects.all()

  return render(request, 'dashboard/customers.html', {
    'customers': customers,
  })

@login_required
def suppliers_dashboard_view(request):
  # Verifica si el usuario es un superusuario
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  # Obtener todos los proveedores
  suppliers = Supplier.objects.all()

  return render(request, 'dashboard/suppliers.html', {
    'suppliers': suppliers,
  })


@login_required
def edit_product(request):
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  product_id = request.GET.get('id')
  product = get_object_or_404(Product, id=product_id)
  suppliers = Supplier.objects.all()

  if request.method == 'POST':
    try:
      # Actualización de los campos del producto
      product.code = request.POST.get('code', product.code)
      product.name = request.POST.get('name', product.name)
      product.description = request.POST.get('description', product.description)
      product.brand = request.POST.get('brand', product.brand)
      product.category = request.POST.get('category', product.category)
      product.price = Decimal(request.POST.get('price', product.price or '0.00'))
      product.discount = int(request.POST.get('discount', product.discount or 0))
      product.number = int(request.POST.get('number', product.number or 0))

      supplier_id = request.POST.get('supplier')
      product.supplier = Supplier.objects.get(id=supplier_id) if supplier_id else None
      product.save()

      # Manejo de nuevas imágenes
      new_images = request.FILES.getlist('new_images')
      ProductImage.objects.bulk_create(
        [ProductImage(product=product, image=image) for image in new_images]
      )

      # Eliminación de imágenes
      images_to_delete = request.POST.getlist('delete_images')
      ProductImage.objects.filter(id__in=images_to_delete, product=product).delete()

      messages.success(request, 'Producto actualizado con éxito.')
      return JsonResponse({'success': True})
    except Exception as e:
      messages.error(request, f'Error al actualizar el producto: {str(e)}')
      return JsonResponse({'success': False, 'error': str(e)})

  context = {
    'product': product,
    'suppliers': suppliers,
    'images': product.images.all(),
  }
  return render(request, 'dashboard/edit_product.html', context)

@login_required
@require_POST
def delete_product_image(request):
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    image_id = request.POST.get('image_id')
    if not image_id:
      return JsonResponse({'success': False, 'error': 'ID de imagen no proporcionado'})
    try:
      image = ProductImage.objects.get(id=image_id)
      image.delete()
      return JsonResponse({'success': True})
    except ProductImage.DoesNotExist:
      return JsonResponse({'success': False, 'error': 'Imagen no encontrada'})
  return JsonResponse({'success': False, 'error': 'Petición inválida'})

@login_required
@require_POST
def delete_product(request):
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  product_id = request.POST.get('product_id')
  try:
    product = Product.objects.get(id=product_id)
    
    # Obtener el nombre del producto para mostrar en el mensaje
    product_name = product.name
    
    # Eliminar el producto
    product.delete()
    
    # Enviar la URL de redirección y el mensaje de éxito
    return JsonResponse({
      'success': True,
      'redirect_url': reverse('dashboard'),  # Redirige al dashboard
      'message': f'Producto "{product_name}" eliminado con éxito.'
    })
  
  except Product.DoesNotExist:
    return JsonResponse({'success': False, 'error': 'Producto no encontrado'})
  except Exception as e:
    return JsonResponse({'success': False, 'error': str(e)})

@login_required
def add_product(request):
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  suppliers = Supplier.objects.all()
  
  if request.method == 'POST':
    try:
      # Create product using form data
      form = ProductForm(request.POST)
      if form.is_valid():
        product = form.save()
        
        # Handle multiple image uploads
        image_files = request.FILES.getlist('image')
        if image_files:
          for image_file in image_files:
            ProductImage.objects.create(product=product, image=image_file)
        
        messages.success(request, 'Producto agregado exitosamente.')
        return JsonResponse({
          'success': True, 
          'redirect_url': reverse('dashboard')  # or 'product_list' if you created that view
        })
      else:
        # If form is not valid, return form errors
        return JsonResponse({
          'success': False, 
          'errors': form.errors
        })
    except Exception as e:
      return JsonResponse({
        'success': False, 
        'error': str(e)
      })
  
  # GET request
  form = ProductForm()
  return render(request, 'dashboard/create_product.html', {
    'form': form, 
    'suppliers': suppliers
  })

# Vista para agregar un suscriptor
@login_required
@csrf_exempt
def add_subscriber(request):
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  if request.method == 'POST':
    email = request.POST.get('email')
    date_subscribed = request.POST.get('date_subscribed')

    # Crear nuevo suscriptor
    new_subscriber = Subscriber(email=email, date_subscribed=date_subscribed)
    new_subscriber.save()

    return JsonResponse({'success': True})

  return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=400)

# Vista para editar un suscriptor
@login_required
@csrf_exempt
def edit_subscriber(request):
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  if request.method == 'POST':
    subscriber_id = request.POST.get('id')
    email = request.POST.get('email')
    date_subscribed = request.POST.get('date_subscribed')

    try:
      subscriber = Subscriber.objects.get(id=subscriber_id)
      subscriber.email = email
      subscriber.date_subscribed = date_subscribed
      subscriber.save()

      return JsonResponse({'success': True})
    except ObjectDoesNotExist:
      return JsonResponse({'success': False, 'error': 'Suscriptor no encontrado'}, status=404)

  return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=400)

# Vista para eliminar un suscriptor
@login_required
@csrf_exempt
def delete_subscriber(request):
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  if request.method == 'POST':
    subscriber_id = request.POST.get('subscriber_id')

    try:
      subscriber = Subscriber.objects.get(id=subscriber_id)
      subscriber.delete()

      return JsonResponse({'success': True})
    except ObjectDoesNotExist:
      return JsonResponse({'success': False, 'error': 'Suscriptor no encontrado'}, status=404)

  return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=400)

#Vista para buscador suscriptores
def search_subscribers(request):
    query = request.GET.get('query', '')
    subscribers = Subscriber.objects.filter(
        Q(email__icontains=query) | Q(date_subscribed__icontains=query)
    )
    data = list(subscribers.values('id', 'email', 'date_subscribed'))
    return JsonResponse(data, safe=False)

#Vista para agregar producto  
@login_required
def add_supplier(request):
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  if request.method == 'POST':
    name = request.POST.get('name')
    email = request.POST.get('email')
    
    # Crear un nuevo proveedor
    Supplier.objects.create(name=name, email=email)
    
    return redirect('suppliers_dashboard_view')

@login_required
def edit_supplier(request, supplier_id):
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  supplier = get_object_or_404(Supplier, id=supplier_id)
  if request.method == 'POST':
    supplier.name = request.POST.get('name')
    supplier.email = request.POST.get('email')
    supplier.save()
    
    return redirect('suppliers_dashboard_view')

@login_required
def delete_supplier(request, supplier_id):
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

  supplier = get_object_or_404(Supplier, id=supplier_id)
  
  if request.method == 'POST':
    supplier.delete()
    # Redirigir a la página de proveedores después de la eliminación
    return redirect('suppliers_dashboard_view')  # Asegúrate de que 'suppliers_list' sea el nombre correcto de tu vista

  return redirect('suppliers_dashboard_view')  # En caso de que no sea un POST, solo redirige.

# Buscador para proovedor
@login_required
def search_suppliers(request):
    query = request.GET.get('query', '')
    suppliers = Supplier.objects.filter(
        Q(name__icontains=query) | Q(email__icontains=query)
    ).values('id', 'name', 'email')
    return JsonResponse(list(suppliers), safe=False)

@login_required
@require_POST
def add_customer(request):
    if not request.user.is_superuser:
        raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")
    form = CustomerForm(request.POST, request.FILES)
    if form.is_valid():
        customer = form.save()
        return JsonResponse({'success': True, 'customer_id': customer.id})
    return JsonResponse({'success': False, 'error': form.errors})

@login_required
@require_POST
def edit_customer(request):
    if not request.user.is_superuser:
        raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")
    customer = get_object_or_404(Customer, id=request.POST.get('id'))
    form = CustomerForm(request.POST, request.FILES, instance=customer)
    if form.is_valid():
        if request.POST.get('remove_avatar') == 'true':
            customer.avatar.delete()
        customer = form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': form.errors})

@login_required
@require_POST
def delete_customer(request):
    if not request.user.is_superuser:
        raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")

    customer_id = request.POST.get('customer_id')
    try:
        customer = Customer.objects.get(id=customer_id)
        customer_name = customer.get_full_name()
        customer.delete()
        return JsonResponse({
            'success': True,
            'redirect_url': reverse('customers_dashboard_view'),
            'message': f'Cliente "{customer_name}" eliminado con éxito.'
        })
    except Customer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cliente no encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# Vista para eliminar una venta
@login_required
@require_POST
def delete_sale(request):
  if not request.user.is_superuser:
    raise PermissionDenied("No tienes permisos suficientes para acceder a esta página")
  sale = get_object_or_404(Sale, id=request.POST.get('sale_id'))
  sale.delete()
  return JsonResponse({'success': True})

@login_required
def orders_list(request):
    orders = Order.objects.all().order_by('-date')
    customers = Customer.objects.all()
    products = Product.objects.all()
    context = {
        'orders': orders,
        'customers': customers,
        'products': products,
    }
    return render(request, 'dashboard/orders.html', context)

@login_required
@csrf_exempt
def add_order(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        total_amount = Decimal(request.POST.get('total'))

        customer = get_object_or_404(Customer, id=customer_id)
        product = get_object_or_404(Product, id=product_id)

        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
            status='pending'
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=400)

@login_required
def view_order(request):
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    # Calcular subtotales
    order_items = order.orderitems.all()
    for item in order_items:
        item.subtotal = item.price * item.quantity

    context = {
        'order': order,
        'order_items': order_items,
    }

    html = render_to_string('dashboard/order_details.html', context)
    return JsonResponse({'success': True, 'html': html})

@login_required
@csrf_exempt
def delete_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=400)

@login_required
def search_orders(request):
    customer_query = request.GET.get('customer', '')
    date_query = request.GET.get('date', '')

    orders = Order.objects.all()

    if customer_query:
        orders = orders.filter(Q(customer__first_name__icontains=customer_query) | Q(customer__last_name__icontains=customer_query))

    if date_query:
        orders = orders.filter(date__date=date_query)

    orders_data = [{
        'id': order.id,
        'date': order.date,
        'customer_name': order.customer.get_full_name(),
        'total_amount': str(order.total_amount),
        'status': order.get_status_display(),
    } for order in orders]

    return JsonResponse(orders_data, safe=False)

