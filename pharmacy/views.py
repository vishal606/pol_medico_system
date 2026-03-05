from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from decimal import Decimal
import json

from .models import Medicine, Supplier, Customer, Bill, BillItem, Category, StockTransaction, UserProfile
from .forms import MedicineForm, SupplierForm, CustomerForm, CategoryForm, LoginForm

PHARMACY_INFO = {
    'name': getattr(settings, 'PHARMACY_NAME', 'POL MEDICO'),
    'name_bn': getattr(settings, 'PHARMACY_NAME_BN', 'পল মেডিকো'),
    'phone': getattr(settings, 'PHARMACY_PHONE', '01722624600'),
    'address': getattr(settings, 'PHARMACY_ADDRESS', 'মৌলভীবাজার'),
    'currency': getattr(settings, 'CURRENCY', '৳'),
}


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'dashboard'))
        form.add_error(None, "ভুল ইউজারনেম বা পাসওয়ার্ড।")
    return render(request, 'pharmacy/login.html', {'form': form, 'pharmacy': PHARMACY_INFO})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    total_medicines = Medicine.objects.filter(is_active=True).count()
    low_stock_count = Medicine.objects.filter(is_active=True, stock_quantity__lte=F('reorder_level')).count()
    total_customers = Customer.objects.count()
    monthly_revenue = Bill.objects.filter(
        status='paid', bill_date__date__gte=month_start
    ).aggregate(total=Sum('grand_total'))['total'] or Decimal('0.00')

    today_revenue = Bill.objects.filter(
        status='paid', bill_date__date=today
    ).aggregate(total=Sum('grand_total'))['total'] or Decimal('0.00')

    recent_bills = Bill.objects.select_related('customer').order_by('-bill_date')[:6]

    days_90 = today + timezone.timedelta(days=90)
    expiring_soon = Medicine.objects.filter(
        is_active=True, expiry_date__lte=days_90, expiry_date__gte=today
    ).order_by('expiry_date')[:5]

    low_stock_medicines = Medicine.objects.filter(
        is_active=True, stock_quantity__lte=F('reorder_level')
    ).order_by('stock_quantity')[:8]

    chart_data = []
    for i in range(5, -1, -1):
        dt = today.replace(day=1) - timezone.timedelta(days=i * 30)
        rev = Bill.objects.filter(
            status='paid', bill_date__year=dt.year, bill_date__month=dt.month,
        ).aggregate(total=Sum('grand_total'))['total'] or 0
        chart_data.append({'month': dt.strftime('%b'), 'revenue': float(rev)})

    context = {
        'total_medicines': total_medicines,
        'low_stock_count': low_stock_count,
        'total_customers': total_customers,
        'monthly_revenue': monthly_revenue,
        'today_revenue': today_revenue,
        'recent_bills': recent_bills,
        'expiring_soon': expiring_soon,
        'low_stock_medicines': low_stock_medicines,
        'chart_data': json.dumps(chart_data),
        'pharmacy': PHARMACY_INFO,
    }
    return render(request, 'pharmacy/dashboard.html', context)


# ── Medicines ─────────────────────────────────────────────────────────────────

@login_required
def medicine_list(request):
    qs = Medicine.objects.select_related('category', 'supplier').filter(is_active=True)
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    stock_filter = request.GET.get('stock', '')

    if q:
        qs = qs.filter(
            Q(name__icontains=q) | Q(generic_name__icontains=q) |
            Q(brand_name__icontains=q) | Q(manufacturer__icontains=q) |
            Q(strength__icontains=q)
        )
    if category:
        qs = qs.filter(category__id=category)
    if stock_filter == 'low':
        qs = qs.filter(stock_quantity__lte=F('reorder_level'))
    elif stock_filter == 'out':
        qs = qs.filter(stock_quantity=0)
    elif stock_filter == 'expiring':
        days_90 = timezone.now().date() + timezone.timedelta(days=90)
        qs = qs.filter(expiry_date__lte=days_90, expiry_date__gte=timezone.now().date())

    categories = Category.objects.all()
    return render(request, 'pharmacy/medicine_list.html', {
        'medicines': qs, 'categories': categories, 'q': q,
        'selected_category': category, 'stock_filter': stock_filter,
        'pharmacy': PHARMACY_INFO,
    })


@login_required
def medicine_create(request):
    form = MedicineForm(request.POST or None)
    if form.is_valid():
        medicine = form.save()
        if medicine.stock_quantity > 0:
            StockTransaction.objects.create(
                medicine=medicine, transaction_type='purchase',
                quantity=medicine.stock_quantity, reference='প্রাথমিক স্টক',
                created_by=request.user,
            )
        messages.success(request, f'"{medicine.display_name}" সফলভাবে যোগ করা হয়েছে।')
        return redirect('medicine_list')
    return render(request, 'pharmacy/medicine_form.html', {'form': form, 'title': 'নতুন ওষুধ যোগ করুন', 'pharmacy': PHARMACY_INFO})


@login_required
def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    old_stock = medicine.stock_quantity
    form = MedicineForm(request.POST or None, instance=medicine)
    if form.is_valid():
        med = form.save()
        diff = med.stock_quantity - old_stock
        if diff != 0:
            StockTransaction.objects.create(
                medicine=med, transaction_type='adjustment', quantity=diff,
                reference='ম্যানুয়াল সমন্বয়', created_by=request.user,
            )
        messages.success(request, f'"{med.display_name}" আপডেট করা হয়েছে।')
        return redirect('medicine_list')
    return render(request, 'pharmacy/medicine_form.html', {'form': form, 'title': 'ওষুধ সম্পাদনা', 'medicine': medicine, 'pharmacy': PHARMACY_INFO})


@login_required
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.is_active = False
        medicine.save()
        messages.success(request, f'"{medicine.name}" মুছে ফেলা হয়েছে।')
        return redirect('medicine_list')
    return render(request, 'pharmacy/confirm_delete.html', {'object': medicine, 'type': 'Medicine', 'pharmacy': PHARMACY_INFO})


@login_required
def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    transactions = medicine.transactions.select_related('created_by').order_by('-created_at')[:20]
    return render(request, 'pharmacy/medicine_detail.html', {'medicine': medicine, 'transactions': transactions, 'pharmacy': PHARMACY_INFO})


# ── Suppliers ─────────────────────────────────────────────────────────────────

@login_required
def supplier_list(request):
    suppliers = Supplier.objects.annotate(medicine_count=Count('medicines'))
    q = request.GET.get('q', '')
    if q:
        suppliers = suppliers.filter(Q(name__icontains=q) | Q(contact_person__icontains=q))
    return render(request, 'pharmacy/supplier_list.html', {'suppliers': suppliers, 'q': q, 'pharmacy': PHARMACY_INFO})


@login_required
def supplier_create(request):
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        s = form.save()
        messages.success(request, f'সাপ্লায়ার "{s.name}" যোগ করা হয়েছে।')
        return redirect('supplier_list')
    return render(request, 'pharmacy/supplier_form.html', {'form': form, 'title': 'নতুন সাপ্লায়ার', 'pharmacy': PHARMACY_INFO})


@login_required
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    form = SupplierForm(request.POST or None, instance=supplier)
    if form.is_valid():
        supplier = form.save()
        messages.success(request, f'"{supplier.name}" আপডেট হয়েছে।')
        return redirect('supplier_list')
    return render(request, 'pharmacy/supplier_form.html', {'form': form, 'title': 'সাপ্লায়ার সম্পাদনা', 'supplier': supplier, 'pharmacy': PHARMACY_INFO})


@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'সাপ্লায়ার মুছে ফেলা হয়েছে।')
        return redirect('supplier_list')
    return render(request, 'pharmacy/confirm_delete.html', {'object': supplier, 'type': 'Supplier', 'pharmacy': PHARMACY_INFO})


# ── Customers ─────────────────────────────────────────────────────────────────

@login_required
def customer_list(request):
    customers = Customer.objects.annotate(bills_count=Count('bills'))
    q = request.GET.get('q', '')
    if q:
        customers = customers.filter(Q(name__icontains=q) | Q(phone__icontains=q))
    return render(request, 'pharmacy/customer_list.html', {'customers': customers, 'q': q, 'pharmacy': PHARMACY_INFO})


@login_required
def customer_create(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        c = form.save()
        messages.success(request, f'রোগী "{c.name}" যোগ করা হয়েছে।')
        return redirect('customer_list')
    return render(request, 'pharmacy/customer_form.html', {'form': form, 'title': 'নতুন রোগী/কাস্টমার', 'pharmacy': PHARMACY_INFO})


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        customer = form.save()
        messages.success(request, f'"{customer.name}" আপডেট হয়েছে।')
        return redirect('customer_list')
    return render(request, 'pharmacy/customer_form.html', {'form': form, 'title': 'তথ্য সম্পাদনা', 'customer': customer, 'pharmacy': PHARMACY_INFO})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'রোগীর তথ্য মুছে ফেলা হয়েছে।')
        return redirect('customer_list')
    return render(request, 'pharmacy/confirm_delete.html', {'object': customer, 'type': 'Customer', 'pharmacy': PHARMACY_INFO})


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    bills = customer.bills.order_by('-bill_date')
    return render(request, 'pharmacy/customer_detail.html', {'customer': customer, 'bills': bills, 'pharmacy': PHARMACY_INFO})


# ── Billing ───────────────────────────────────────────────────────────────────

@login_required
def bill_list(request):
    bills = Bill.objects.select_related('customer', 'created_by').order_by('-bill_date')
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    if q:
        bills = bills.filter(Q(invoice_number__icontains=q) | Q(customer__name__icontains=q))
    if status:
        bills = bills.filter(status=status)
    return render(request, 'pharmacy/bill_list.html', {'bills': bills, 'q': q, 'status': status, 'pharmacy': PHARMACY_INFO})


@login_required
def bill_create(request):
    customers = Customer.objects.all()
    medicines = Medicine.objects.filter(is_active=True, stock_quantity__gt=0).select_related('category').order_by('name')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'error': 'Invalid data'}, status=400)

        customer_id = data.get('customer_id')
        items = data.get('items', [])
        discount = Decimal(str(data.get('discount', '0')))
        tax = Decimal(str(data.get('tax', '0')))
        notes = data.get('notes', '')

        if not items:
            return JsonResponse({'error': 'কোনো ওষুধ নির্বাচন করা হয়নি।'}, status=400)

        customer = None
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                pass

        bill = Bill.objects.create(
            customer=customer, created_by=request.user,
            discount_percent=discount, tax_percent=tax,
            notes=notes, status='paid',
        )

        for item_data in items:
            try:
                medicine = Medicine.objects.get(id=item_data['medicine_id'])
            except Medicine.DoesNotExist:
                bill.delete()
                return JsonResponse({'error': 'ওষুধ পাওয়া যায়নি।'}, status=400)

            qty = int(item_data['quantity'])
            price = Decimal(str(item_data['price']))

            if qty > medicine.stock_quantity:
                bill.delete()
                return JsonResponse({'error': f'{medicine.name} এর পর্যাপ্ত স্টক নেই। উপলব্ধ: {medicine.stock_quantity}'}, status=400)

            BillItem.objects.create(
                bill=bill, medicine=medicine,
                medicine_name=medicine.display_name,
                quantity=qty, unit_price=price,
            )
            medicine.stock_quantity -= qty
            medicine.save()
            StockTransaction.objects.create(
                medicine=medicine, transaction_type='sale',
                quantity=-qty, reference=bill.invoice_number,
                created_by=request.user,
            )

        bill.calculate_totals()
        return JsonResponse({'success': True, 'invoice_number': bill.invoice_number, 'bill_id': bill.id})

    return render(request, 'pharmacy/bill_create.html', {
        'customers': customers, 'medicines': medicines, 'pharmacy': PHARMACY_INFO
    })


@login_required
def bill_detail(request, pk):
    bill = get_object_or_404(Bill.objects.select_related('customer', 'created_by'), pk=pk)
    items = bill.items.select_related('medicine')
    return render(request, 'pharmacy/bill_detail.html', {'bill': bill, 'items': items, 'pharmacy': PHARMACY_INFO})


@login_required
def bill_print(request, pk):
    bill = get_object_or_404(Bill.objects.select_related('customer'), pk=pk)
    items = bill.items.all()
    return render(request, 'pharmacy/bill_print.html', {'bill': bill, 'items': items, 'pharmacy': PHARMACY_INFO})


# ── Reports ───────────────────────────────────────────────────────────────────

@login_required
def reports(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)

    daily_revenue = Bill.objects.filter(status='paid', bill_date__date=today).aggregate(t=Sum('grand_total'))['t'] or 0
    monthly_revenue = Bill.objects.filter(status='paid', bill_date__date__gte=month_start).aggregate(t=Sum('grand_total'))['t'] or 0
    yearly_revenue = Bill.objects.filter(status='paid', bill_date__date__gte=year_start).aggregate(t=Sum('grand_total'))['t'] or 0
    total_bills = Bill.objects.filter(status='paid').count()
    avg_bill = (float(yearly_revenue) / total_bills) if total_bills else 0

    top_medicines = BillItem.objects.values('medicine_name').annotate(
        total_qty=Sum('quantity')
    ).order_by('-total_qty')[:10]

    chart_data = []
    for i in range(11, -1, -1):
        dt = today.replace(day=1) - timezone.timedelta(days=i * 30)
        rev = Bill.objects.filter(
            status='paid', bill_date__year=dt.year, bill_date__month=dt.month,
        ).aggregate(t=Sum('grand_total'))['t'] or 0
        chart_data.append({'month': dt.strftime('%b'), 'revenue': float(rev)})

    low_stock_items = Medicine.objects.filter(is_active=True, stock_quantity__lte=F('reorder_level'))
    expiring_items = Medicine.objects.filter(
        is_active=True,
        expiry_date__lte=today + timezone.timedelta(days=90),
        expiry_date__gte=today
    ).order_by('expiry_date')

    context = {
        'daily_revenue': daily_revenue,
        'monthly_revenue': monthly_revenue,
        'yearly_revenue': yearly_revenue,
        'total_bills': total_bills,
        'avg_bill': avg_bill,
        'top_medicines': top_medicines,
        'chart_data': json.dumps(chart_data),
        'low_stock_items': low_stock_items,
        'expiring_items': expiring_items,
        'total_medicines': Medicine.objects.filter(is_active=True).count(),
        'total_customers': Customer.objects.count(),
        'total_suppliers': Supplier.objects.filter(status='active').count(),
        'pharmacy': PHARMACY_INFO,
    }
    return render(request, 'pharmacy/reports.html', context)


# ── AJAX ──────────────────────────────────────────────────────────────────────

@login_required
def get_medicine_price(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return JsonResponse({
        'price': str(medicine.selling_price),
        'stock': medicine.stock_quantity,
        'name': medicine.display_name,
    })
