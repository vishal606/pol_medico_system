from django.contrib import admin
from django.utils.html import format_html
from .models import Medicine, Supplier, Customer, Bill, BillItem, Category, StockTransaction, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone']
    list_filter = ['role']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'status']
    list_filter = ['status']
    search_fields = ['name']


class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 0
    readonly_fields = ['medicine_name', 'quantity', 'unit_price']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'strength', 'dosage_form', 'manufacturer', 'category', 'stock_quantity', 'selling_price', 'stock_badge', 'is_active']
    list_filter = ['category', 'dosage_form', 'is_active']
    search_fields = ['name', 'generic_name', 'brand_name', 'manufacturer']
    list_editable = ['stock_quantity', 'is_active']

    def stock_badge(self, obj):
        if obj.stock_quantity == 0:
            return format_html('<span style="color:red;font-weight:bold">স্টক শেষ</span>')
        elif obj.is_low_stock:
            return format_html('<span style="color:orange;font-weight:bold">কম স্টক</span>')
        return format_html('<span style="color:green">✓</span>')
    stock_badge.short_description = "স্টক"


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'created_at']
    search_fields = ['name', 'phone']


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer', 'bill_date', 'grand_total', 'status']
    list_filter = ['status', 'bill_date']
    search_fields = ['invoice_number', 'customer__name']
    readonly_fields = ['invoice_number']
    inlines = [BillItemInline]


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'transaction_type', 'quantity', 'reference', 'created_at']
    list_filter = ['transaction_type']
    search_fields = ['medicine__name']
