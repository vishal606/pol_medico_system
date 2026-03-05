from django import forms
from .models import Medicine, Supplier, Customer, Bill, BillItem, Category


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username', 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'generic_name', 'brand_name', 'dosage_form', 'strength', 'manufacturer',
                  'category', 'supplier', 'batch_number', 'stock_quantity', 'reorder_level',
                  'purchase_price', 'selling_price', 'expiry_date', 'manufacture_date', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ওষুধের নাম'}),
            'generic_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Generic name (e.g. Paracetamol)'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brand name (e.g. Napa)'}),
            'dosage_form': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tablet / Syrup / Capsule / Injection'}),
            'strength': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '500mg / 250mg/5ml'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Square / Beximco / ACME'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'supplier': forms.Select(attrs={'class': 'form-input'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-input'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'manufacture_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': '2'}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone', 'email', 'address', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': '3'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address', 'date_of_birth']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'রোগীর নাম'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '01XXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': '2'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': '2'}),
        }
