from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


class UserProfile(models.Model):
    ROLES = [
        ('admin', 'Administrator'),
        ('pharmacist', 'Pharmacist / ফার্মাসিস্ট'),
        ('staff', 'Staff / স্টাফ'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLES, default='staff')
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "User Profile"


class Supplier(models.Model):
    STATUS_CHOICES = [('active', 'সক্রিয়'), ('inactive', 'নিষ্ক্রিয়')]
    name = models.CharField(max_length=200, unique=True)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']


class Medicine(models.Model):
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    brand_name = models.CharField(max_length=200, blank=True)
    dosage_form = models.CharField(max_length=100, blank=True)  # Tablet, Syrup, etc.
    strength = models.CharField(max_length=100, blank=True)     # 500mg, 5ml, etc.
    manufacturer = models.CharField(max_length=200, blank=True) # Square, Beximco, etc.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='medicines')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='medicines')
    batch_number = models.CharField(max_length=100, blank=True)
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    reorder_level = models.IntegerField(default=50, validators=[MinValueValidator(0)])
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    expiry_date = models.DateField(null=True, blank=True)
    manufacture_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.strength}" if self.strength else self.name

    @property
    def display_name(self):
        parts = [self.name]
        if self.strength:
            parts.append(self.strength)
        if self.dosage_form:
            parts.append(f"({self.dosage_form})")
        return ' '.join(parts)

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.reorder_level

    @property
    def is_expired(self):
        if not self.expiry_date:
            return False
        return self.expiry_date < timezone.now().date()

    @property
    def is_expiring_soon(self):
        if not self.expiry_date:
            return False
        days_90 = timezone.now().date() + timezone.timedelta(days=90)
        return self.expiry_date <= days_90 and not self.is_expired

    class Meta:
        ordering = ['name']


class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def total_purchases(self):
        return self.bills.filter(status='paid').aggregate(
            total=models.Sum('grand_total')
        )['total'] or Decimal('0.00')

    class Meta:
        ordering = ['name']


class Bill(models.Model):
    STATUS_CHOICES = [
        ('paid', 'পরিশোধিত'),
        ('pending', 'বাকি'),
        ('cancelled', 'বাতিল'),
    ]
    invoice_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='bills')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='bills')
    bill_date = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='paid')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last = Bill.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.invoice_number = f"PM-{next_id:05d}"
        super().save(*args, **kwargs)

    def calculate_totals(self):
        self.subtotal = sum(item.line_total for item in self.items.all())
        self.discount_amount = (self.subtotal * self.discount_percent / 100).quantize(Decimal('0.01'))
        taxable = self.subtotal - self.discount_amount
        self.tax_amount = (taxable * self.tax_percent / 100).quantize(Decimal('0.01'))
        self.grand_total = taxable + self.tax_amount
        self.save()

    def __str__(self):
        return self.invoice_number

    class Meta:
        ordering = ['-bill_date']


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True, related_name='bill_items')
    medicine_name = models.CharField(max_length=200)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.medicine_name} x{self.quantity}"


class StockTransaction(models.Model):
    TYPE_CHOICES = [
        ('purchase', 'ক্রয়'),
        ('sale', 'বিক্রয়'),
        ('adjustment', 'সমন্বয়'),
        ('return', 'ফেরত'),
        ('expired', 'মেয়াদোত্তীর্ণ'),
    ]
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantity = models.IntegerField()
    reference = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine.name} | {self.transaction_type} | {self.quantity}"

    class Meta:
        ordering = ['-created_at']
