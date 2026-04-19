from django.shortcuts import render,redirect,get_object_or_404
from django.db import models
from django.db.models import Sum, Count
from .models import Product, Sale
from .forms import ProductForm,SaleForm,StockAdjustmentForm
from django.contrib.auth.decorators import login_required 

@login_required
def dashboard(request):
    total_products = Product.objects.count()
    total_sales = Sale.objects.aggregate(total=Sum('quantity_sold'))['total'] or 0

    low_stock = Product.objects.filter(quantity__lte=models.F('minimum_stock')).count()

    high_demand = Sale.objects.values('product').annotate(total=Sum('quantity_sold')).filter(total__gt=5).count()

    sales_data = Sale.objects.values('product__name').annotate(total=Sum('quantity_sold'))

    product_names = [item['product__name'] for item in sales_data]
    sales_values = [item['total'] for item in sales_data]

    context = {
        'total_products': total_products,
        'total_sales': total_sales,
        'low_stock': low_stock,
        'high_demand': high_demand,
        'sales_summary': zip(product_names, sales_values),
    }

    return render(request, 'dashboard.html', context)

@login_required
def product_list(request):
    query = request.GET.get('q') 

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    demand_data = Sale.objects.values('product').annotate(total_sold=Sum('quantity_sold'))
    demand_dict = {item['product']: item['total_sold'] for item in demand_data}

    for product in products:
        total_sold = demand_dict.get(product.id, 0)

        if total_sold > 5:
            product.demand = "High"
        elif total_sold == 0:
            product.demand = "New"
        else:
            product.demand = "Normal"

        if product.quantity <= product.minimum_stock:
            if product.demand == "High":
                product.restock = "Urgent"
            else:
                product.restock = "Needed"
        else:
            product.restock = "OK"

    return render(request, 'product_list.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

@login_required
def update_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'update_product.html', {'form': form})

@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'delete_product.html', {'product': product})

@login_required
def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            try:
                form.save()  
                return redirect('product_list')
            except ValueError as e:
                form.add_error(None, str(e)) 
    else:
        form = SaleForm()

    return render(request, 'add_sale.html', {'form': form})

@login_required
def stock_adjustment(request):
    if request.method == 'POST':
        form = StockAdjustmentForm(request.POST)
        if form.is_valid():
            try:
                form.save()   
                return redirect('product_list')
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = StockAdjustmentForm()

    return render(request, 'stock_adjustment.html', {'form': form})
