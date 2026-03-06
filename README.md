# 💊 POL MEDICO — পল মেডিকো
### Pharmacy Management System | ফার্মেসি ম্যানেজমেন্ট সিস্টেম

> **Django 4.2 + REST API | Currency: ৳ BDT | Bilingual UI (বাংলা + English)**

📞 **01722624600**
📍 টাউন দেওয়ানী জামে মসজিদ ও পান্সী রেষ্টুরেন্ট এর পুর্ব পার্শ্বে, কোর্ট রোড, চৌমুহনা, মৌলভীবাজার

---

## 📋 Table of Contents
- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Login Credentials](#-login-credentials)
- [Project Structure](#-project-structure)
- [Medicine Data](#-medicine-data-medexcombd)
- [Usage Guide](#-usage-guide)
- [REST API](#-rest-api)
- [Troubleshooting](#-troubleshooting)
- [Customization](#-customization)

---

## ✨ Features

| Feature | Description |
|---|---|
| 💊 **ওষুধ ব্যবস্থাপনা** | 45+ real Bangladeshi medicines from medex.com.bd. Track stock, expiry, pricing in ৳ |
| 🧾 **বিলিং সিস্টেম** | Dynamic invoice builder with live ৳ totals, discount, VAT, printable Bangla receipts |
| 📦 **স্টক ট্র্যাকিং** | Real-time stock updates on every sale, low stock alerts, 90-day expiry warnings |
| 👥 **রোগী ব্যবস্থাপনা** | Patient profiles with full purchase history and total spend in ৳ |
| 🏭 **সাপ্লায়ার** | 8 major Bangladeshi pharma companies preloaded (Square, Beximco, ACME, Renata…) |
| 📊 **রিপোর্ট** | Daily/monthly/yearly revenue in ৳, top medicines, 12-month chart |
| 🔌 **REST API** | Full REST API at `/api/` with token authentication |
| 🔐 **নিরাপত্তা** | Role-based access: Admin, Pharmacist, Staff |

---

## 🖥️ Requirements

- Python **3.8+**
- Django **4.2.x**
- djangorestframework **3.14+**
- SQLite (default) — upgradeable to PostgreSQL
- Any modern browser (Chrome, Firefox, Safari, Edge)

---

## 🚀 Installation

### Step 1 — Extract the ZIP
Download `pol_medico_django.zip` and extract it. Then open Terminal and navigate into the project:

```bash
cd pol_medico_system
```

### Step 2 — Create & Activate Virtual Environment

**macOS / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set Up Database
```bash
python manage.py migrate
```

### Step 5 — Load Sample Data (Bangladeshi Medicines)
```bash
python manage.py seed_data
```

### Step 6 — Run the Server
```bash
python manage.py runserver
```

Open your browser and go to: **http://127.0.0.1:8000**

> ⚠️ **Anaconda Users:** Activate your venv first (`source venv/bin/activate`), then use `pip install`. Do **not** use `conda install`.

---

## 🔐 Login Credentials

| Role | Username | Password |
|---|---|---|
| Admin (সব অ্যাক্সেস) | `admin` | `admin123` |
| Staff (সাধারণ) | `staff` | `staff123` |

> Change default passwords immediately in production via `/admin/`.

---

## 📁 Project Structure

```
pol_medico_system/
├── manage.py
├── requirements.txt
├── setup.sh
├── pol_medico_system/
│   ├── settings.py          # Pharmacy info, timezone, currency config
│   ├── urls.py
│   └── wsgi.py
└── pharmacy/
    ├── models.py            # Medicine, Bill, Customer, Supplier, etc.
    ├── views.py             # Dashboard, medicines, billing, reports
    ├── urls.py              # Web routes
    ├── api_urls.py          # REST API routes
    ├── forms.py
    ├── admin.py
    ├── templates/pharmacy/  # 16 HTML templates (Bangla UI)
    │   ├── base.html
    │   ├── login.html
    │   ├── dashboard.html
    │   ├── medicine_list.html
    │   ├── medicine_form.html
    │   ├── medicine_detail.html
    │   ├── bill_create.html
    │   ├── bill_list.html
    │   ├── bill_detail.html
    │   ├── bill_print.html   # Bangla print receipt
    │   ├── supplier_list.html
    │   ├── supplier_form.html
    │   ├── customer_list.html
    │   ├── customer_form.html
    │   ├── customer_detail.html
    │   ├── reports.html
    │   └── confirm_delete.html
    └── management/commands/
        └── seed_data.py     # Loads 45+ Bangladeshi medicines
```

---

## 💊 Medicine Data (medex.com.bd)

Real medicines preloaded from **medex.com.bd** — Bangladesh's leading medicine index. All prices in ৳ BDT.

| Category | Sample Medicines |
|---|---|
| Analgesic / ব্যথানাশক | Napa 500mg, Ace 500mg, Napa Extra, Ace Plus |
| Antibiotic / এন্টিবায়োটিক | Azith 500mg, Moxacil 500mg, Zimax 200mg, Filmet 400mg |
| Antidiabetic / ডায়াবেটিস | Glucomin 500mg, Glucomin XR 1000mg, Glimestar 2mg, Jalra 50mg |
| Antihypertensive / উচ্চ রক্তচাপ | Amdocal 5mg, Losacar 50mg, Enace 5mg |
| Gastrointestinal / পেটের ওষুধ | Seclo 20mg, Pantonix 40mg, Domperi 10mg, Ranitid 150mg |
| Antihistamine / এলার্জি | Cetrizin 10mg, Rihist 120mg, Alercet Syrup |
| Vitamin & Supplement | Vitamin C 500mg, Neurobion, A-Cal D, Zinca Syrup |
| Respiratory / শ্বাস-প্রশ্বাস | Sultolin Inhaler, Montek 10mg, Ambrox Syrup |
| Statin / কোলেস্টেরল | Statin 20mg, Lipovas 10mg |
| Oral Rehydration / স্যালাইন | ORS 27.9g/sachet |
| Antifungal / ছত্রাকনাশক | Flucon 150mg |
| Dermatology / চর্মরোগ | Fusiderm Cream 2% |

**Manufacturers included:** Square Pharmaceuticals, Beximco Pharmaceuticals, ACME Laboratories, Renata PLC, Incepta Pharmaceuticals, ACI Limited, Opsonin Pharma

---

## 📖 Usage Guide

### নতুন বিক্রয় — Creating a New Sale
1. Click **নতুন বিক্রয়** in the sidebar
2. Select customer (optional — Walk-in supported)
3. Click **+ আইটেম যোগ** to add medicines
4. Choose medicine, set quantity (stock is auto-checked)
5. Apply discount % or VAT % if needed
6. Click **চালান তৈরি করুন** to generate invoice
7. Print the Bangla receipt from the invoice page

### নতুন ওষুধ যোগ — Adding a Medicine
1. Go to **ওষুধ তালিকা** → click **+ নতুন ওষুধ**
2. Fill in: name, generic name, brand, dosage form, strength
3. Enter purchase price (৳) and selling price (৳)
4. Set stock quantity, reorder level, expiry date
5. Select supplier and category → save

### রিপোর্ট — Viewing Reports
- Go to **রিপোর্ট** in the sidebar
- View daily / monthly / yearly revenue in ৳
- See top 10 best-selling medicines
- Check low stock and expiring medicine alerts
- 12-month bar chart for revenue trends

---

## 🔌 REST API

Base URL: `http://127.0.0.1:8000/api/`

| Endpoint | Method | Description |
|---|---|---|
| `/api/medicines/` | GET, POST | List / create medicines |
| `/api/medicines/{id}/` | GET, PUT, DELETE | Medicine detail |
| `/api/bills/` | GET, POST | List / create invoices |
| `/api/customers/` | GET, POST | List / create customers |
| `/api/suppliers/` | GET, POST | List / create suppliers |
| `/api/categories/` | GET, POST | List / create categories |
| `/api/auth/token/` | POST | Get auth token |

### Token Authentication

```bash
# Get token
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -d '{"username": "admin", "password": "admin123"}' \
  -H "Content-Type: application/json"

# Use token
curl http://127.0.0.1:8000/api/medicines/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---

## 🛠️ Troubleshooting

| Error | Solution |
|---|---|
| `No module named 'django'` | Run `source venv/bin/activate` then `pip install -r requirements.txt` |
| `No module named 'rest_framework'` | Run `pip install djangorestframework` |
| Port 8000 already in use | Run `python manage.py runserver 8001` |
| `OperationalError: no such table` | Run `python manage.py migrate` |
| Migrations not applied | Run `python manage.py makemigrations` then `python manage.py migrate` |
| Login not working | Run `python manage.py seed_data` again |
| Static files not loading | Run `python manage.py collectstatic` (production only) |

---

## ⚙️ Customization

Edit `pol_medico_system/settings.py` to update pharmacy details:

```python
# Pharmacy Configuration
PHARMACY_NAME    = 'POL MEDICO'
PHARMACY_NAME_BN = 'পল মেডিকো'
PHARMACY_PHONE   = '01722624600'
PHARMACY_ADDRESS = 'কোর্ট রোড, চৌমুহনা, মৌলভীবাজার'
CURRENCY         = '৳'
CURRENCY_CODE    = 'BDT'
```

---

## 📞 যোগাযোগ | Contact

**POL MEDICO — পল মেডিকো**
📞 01722624600
📍 টাউন দেওয়ানী জামে মসজিদ ও পান্সী রেষ্টুরেন্ট এর পুর্ব পার্শ্বে
কোর্ট রোড, চৌমুহনা, মৌলভীবাজার

---

*POL MEDICO Pharmacy Management System v1.0 | Built with Django 4.2*
