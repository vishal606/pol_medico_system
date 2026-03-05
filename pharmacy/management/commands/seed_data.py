"""
Seed command for POL MEDICO — পল মেডিকো
Real Bangladeshi medicines sourced from medex.com.bd
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pharmacy.models import Category, Supplier, Medicine, Customer, UserProfile
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seeds database with Bangladeshi pharmacy data for POL MEDICO'

    def handle(self, *args, **options):
        self.stdout.write('\n  💊 পল মেডিকো — ডেটা লোড হচ্ছে...\n')

        # ── Users ──────────────────────────────────────────────────────────────
        admin_user, _ = User.objects.get_or_create(username='admin', defaults={
            'email': 'admin@polmedico.com', 'is_staff': True, 'is_superuser': True,
            'first_name': 'Admin',
        })
        admin_user.set_password('admin123')
        admin_user.save()
        UserProfile.objects.get_or_create(user=admin_user, defaults={'role': 'admin'})

        staff_user, _ = User.objects.get_or_create(username='staff', defaults={
            'email': 'staff@polmedico.com', 'first_name': 'Staff',
        })
        staff_user.set_password('staff123')
        staff_user.save()
        UserProfile.objects.get_or_create(user=staff_user, defaults={'role': 'staff'})

        self.stdout.write('  ✓ Users: admin/admin123, staff/staff123')

        # ── Categories ─────────────────────────────────────────────────────────
        cat_names = [
            'Analgesic / ব্যথানাশক',
            'Antibiotic / এন্টিবায়োটিক',
            'Antidiabetic / ডায়াবেটিস',
            'Antihypertensive / উচ্চ রক্তচাপ',
            'Gastrointestinal / পেটের ওষুধ',
            'Antihistamine / এলার্জি',
            'Vitamin & Supplement / ভিটামিন',
            'Respiratory / শ্বাস-প্রশ্বাস',
            'Antifungal / ছত্রাকনাশক',
            'Cardiovascular / হৃদরোগ',
            'Neurological / স্নায়বিক',
            'Antacid / এন্টাসিড',
            'Oral Rehydration / স্যালাইন',
            'Ophthalmology / চোখের ওষুধ',
            'Dermatology / চর্মরোগ',
            'Hormonal / হরমোন',
            'Statin / কোলেস্টেরল',
            'NSAID / প্রদাহনাশক',
        ]
        categories = {}
        for name in cat_names:
            cat, _ = Category.objects.get_or_create(name=name)
            categories[name] = cat
        self.stdout.write(f'  ✓ {len(cat_names)} categories created')

        # ── Suppliers (Bangladeshi pharma companies) ───────────────────────────
        supplier_data = [
            ('Square Pharmaceuticals PLC', 'Sales Team', '02-8833047', 'info@squarepharma.com.bd', 'Manikgonj, Dhaka'),
            ('Beximco Pharmaceuticals Ltd.', 'Sales Dept.', '02-9893308', 'info@beximcopharma.com', 'Tongi, Gazipur'),
            ('ACME Laboratories Ltd.', 'Sales Team', '02-7914001', 'info@acmelab.com', 'Dhamrai, Dhaka'),
            ('Renata PLC', 'Sales Dept.', '02-8878501', 'info@renata.com', 'Mirpur, Dhaka'),
            ('Incepta Pharmaceuticals Ltd.', 'Sales Team', '02-7914020', 'info@inceptapharma.com', 'Zirabo, Savar'),
            ('ACI Limited', 'Sales Dept.', '02-8828774', 'info@aci-bd.com', 'Tejgaon, Dhaka'),
            ('Opsonin Pharma Ltd.', 'Sales Team', '02-7791022', 'info@opsonin.com', 'Mirpur, Dhaka'),
            ('Healthcare Pharma Ltd.', 'Local Rep', '01711-000001', 'local@healthcare.com', 'Moulvibazar'),
        ]
        suppliers = {}
        for name, contact, phone, email, address in supplier_data:
            sup, _ = Supplier.objects.get_or_create(name=name, defaults={
                'contact_person': contact, 'phone': phone, 'email': email, 'address': address,
            })
            suppliers[name] = sup
        self.stdout.write(f'  ✓ {len(supplier_data)} Bangladeshi suppliers created')

        # ── Medicines (real brands from medex.com.bd) ──────────────────────────
        # Format: (name, generic, brand, form, strength, manufacturer, category, supplier, stock, reorder, purchase, sell, expiry)
        medicines_data = [
            # Analgesics
            ('Napa', 'Paracetamol', 'Napa', 'Tablet', '500 mg', 'Beximco Pharmaceuticals Ltd.', 'Analgesic / ব্যথানাশক', 'Beximco Pharmaceuticals Ltd.', 500, 100, 1.50, 2.00, '2027-06-30'),
            ('Napa Extra', 'Paracetamol + Caffeine', 'Napa Extra', 'Tablet', '500 mg+65 mg', 'Beximco Pharmaceuticals Ltd.', 'Analgesic / ব্যথানাশক', 'Beximco Pharmaceuticals Ltd.', 300, 80, 2.00, 3.00, '2027-04-30'),
            ('Ace', 'Paracetamol', 'Ace', 'Tablet', '500 mg', 'Square Pharmaceuticals PLC', 'Analgesic / ব্যথানাশক', 'Square Pharmaceuticals PLC', 450, 100, 1.50, 2.00, '2027-08-30'),
            ('Ace Plus', 'Paracetamol + Caffeine', 'Ace Plus', 'Tablet', '500 mg+65 mg', 'Square Pharmaceuticals PLC', 'Analgesic / ব্যথানাশক', 'Square Pharmaceuticals PLC', 200, 60, 2.00, 3.00, '2027-05-15'),
            ('Apanil', 'Paracetamol', 'Apanil', 'Syrup', '120 mg/5 ml', 'ACME Laboratories Ltd.', 'Analgesic / ব্যথানাশক', 'ACME Laboratories Ltd.', 120, 30, 30.00, 45.00, '2026-09-30'),
            ('Nurofen', 'Ibuprofen', 'Nurofen', 'Tablet', '400 mg', 'Square Pharmaceuticals PLC', 'NSAID / প্রদাহনাশক', 'Square Pharmaceuticals PLC', 250, 60, 5.00, 8.00, '2027-03-31'),
            ('Flamex', 'Ibuprofen', 'Flamex', 'Tablet', '400 mg', 'Beximco Pharmaceuticals Ltd.', 'NSAID / প্রদাহনাশক', 'Beximco Pharmaceuticals Ltd.', 200, 50, 4.50, 7.00, '2027-01-15'),

            # Antibiotics
            ('Azith', 'Azithromycin', 'Azith', 'Tablet', '500 mg', 'Square Pharmaceuticals PLC', 'Antibiotic / এন্টিবায়োটিক', 'Square Pharmaceuticals PLC', 80, 30, 35.00, 55.00, '2026-12-31'),
            ('Azimax', 'Azithromycin', 'Azimax', 'Tablet', '500 mg', 'ACME Laboratories Ltd.', 'Antibiotic / এন্টিবায়োটিক', 'ACME Laboratories Ltd.', 60, 25, 33.00, 50.00, '2027-02-28'),
            ('Moxacil', 'Amoxicillin', 'Moxacil', 'Capsule', '500 mg', 'Square Pharmaceuticals PLC', 'Antibiotic / এন্টিবায়োটিক', 'Square Pharmaceuticals PLC', 150, 50, 8.00, 12.00, '2027-01-31'),
            ('Clavam', 'Amoxicillin+Clavulanic Acid', 'Clavam', 'Tablet', '500 mg+125 mg', 'Square Pharmaceuticals PLC', 'Antibiotic / এন্টিবায়োটিক', 'Square Pharmaceuticals PLC', 60, 20, 38.00, 60.00, '2026-11-30'),
            ('Zimax', 'Cefixime', 'Zimax', 'Capsule', '200 mg', 'Square Pharmaceuticals PLC', 'Antibiotic / এন্টিবায়োটিক', 'Square Pharmaceuticals PLC', 80, 25, 30.00, 48.00, '2027-03-31'),
            ('Cef-3', 'Cefixime', 'Cef-3', 'Capsule', '200 mg', 'Incepta Pharmaceuticals Ltd.', 'Antibiotic / এন্টিবায়োটিক', 'Incepta Pharmaceuticals Ltd.', 70, 20, 28.00, 45.00, '2026-10-31'),
            ('Cipro', 'Ciprofloxacin', 'Cipro', 'Tablet', '500 mg', 'Beximco Pharmaceuticals Ltd.', 'Antibiotic / এন্টিবায়োটিক', 'Beximco Pharmaceuticals Ltd.', 15, 30, 10.00, 16.00, '2026-08-15'),

            # Antidiabetic
            ('Glucomin', 'Metformin HCl', 'Glucomin', 'Tablet', '500 mg', 'Square Pharmaceuticals PLC', 'Antidiabetic / ডায়াবেটিস', 'Square Pharmaceuticals PLC', 350, 80, 3.00, 5.00, '2027-07-31'),
            ('Glucomin XR', 'Metformin HCl', 'Glucomin XR', 'Tablet', '1000 mg', 'Square Pharmaceuticals PLC', 'Antidiabetic / ডায়াবেটিস', 'Square Pharmaceuticals PLC', 200, 50, 6.00, 9.00, '2027-06-30'),
            ('Formet', 'Metformin HCl', 'Formet', 'Tablet', '500 mg', 'ACME Laboratories Ltd.', 'Antidiabetic / ডায়াবেটিস', 'ACME Laboratories Ltd.', 280, 70, 2.80, 4.50, '2027-05-31'),
            ('Glimestar', 'Glimepiride', 'Glimestar', 'Tablet', '2 mg', 'Square Pharmaceuticals PLC', 'Antidiabetic / ডায়াবেটিস', 'Square Pharmaceuticals PLC', 160, 40, 5.00, 8.00, '2027-04-30'),
            ('Jalra', 'Vildagliptin', 'Jalra', 'Tablet', '50 mg', 'Novartis', 'Antidiabetic / ডায়াবেটিস', 'Healthcare Pharma Ltd.', 50, 20, 60.00, 95.00, '2026-09-30'),

            # Antihypertensive
            ('Amdocal', 'Amlodipine Besylate', 'Amdocal', 'Tablet', '5 mg', 'Square Pharmaceuticals PLC', 'Antihypertensive / উচ্চ রক্তচাপ', 'Square Pharmaceuticals PLC', 180, 50, 4.00, 6.50, '2027-08-31'),
            ('Norvasc', 'Amlodipine Besylate', 'Norvasc', 'Tablet', '5 mg', 'Pfizer', 'Antihypertensive / উচ্চ রক্তচাপ', 'Healthcare Pharma Ltd.', 12, 25, 16.00, 25.00, '2025-12-31'),
            ('Losacar', 'Losartan Potassium', 'Losacar', 'Tablet', '50 mg', 'Square Pharmaceuticals PLC', 'Antihypertensive / উচ্চ রক্তচাপ', 'Square Pharmaceuticals PLC', 140, 40, 7.00, 11.00, '2027-02-28'),
            ('Enace', 'Enalapril Maleate', 'Enace', 'Tablet', '5 mg', 'Square Pharmaceuticals PLC', 'Antihypertensive / উচ্চ রক্তচাপ', 'Square Pharmaceuticals PLC', 120, 35, 4.50, 7.00, '2027-03-31'),

            # GI
            ('Seclo', 'Omeprazole', 'Seclo', 'Capsule', '20 mg', 'Square Pharmaceuticals PLC', 'Gastrointestinal / পেটের ওষুধ', 'Square Pharmaceuticals PLC', 200, 50, 5.00, 8.00, '2027-01-31'),
            ('Losectil', 'Omeprazole', 'Losectil', 'Capsule', '20 mg', 'Beximco Pharmaceuticals Ltd.', 'Gastrointestinal / পেটের ওষুধ', 'Beximco Pharmaceuticals Ltd.', 160, 40, 5.00, 7.50, '2027-04-30'),
            ('Pantonix', 'Pantoprazole', 'Pantonix', 'Tablet', '40 mg', 'Incepta Pharmaceuticals Ltd.', 'Gastrointestinal / পেটের ওষুধ', 'Incepta Pharmaceuticals Ltd.', 130, 35, 8.00, 13.00, '2027-05-31'),
            ('Ranitid', 'Ranitidine HCl', 'Ranitid', 'Tablet', '150 mg', 'Square Pharmaceuticals PLC', 'Antacid / এন্টাসিড', 'Square Pharmaceuticals PLC', 250, 60, 2.50, 4.00, '2027-06-30'),
            ('Domperi', 'Domperidone', 'Domperi', 'Tablet', '10 mg', 'Square Pharmaceuticals PLC', 'Gastrointestinal / পেটের ওষুধ', 'Square Pharmaceuticals PLC', 180, 50, 3.00, 5.00, '2027-04-30'),

            # Antihistamine
            ('Cetrizin', 'Cetirizine HCl', 'Cetrizin', 'Tablet', '10 mg', 'Square Pharmaceuticals PLC', 'Antihistamine / এলার্জি', 'Square Pharmaceuticals PLC', 220, 60, 3.00, 5.00, '2027-07-31'),
            ('Rihist', 'Fexofenadine HCl', 'Rihist', 'Tablet', '120 mg', 'Renata PLC', 'Antihistamine / এলার্জি', 'Renata PLC', 100, 30, 12.00, 18.00, '2027-03-31'),
            ('Alercet', 'Cetirizine HCl', 'Alercet', 'Syrup', '5 mg/5 ml', 'Square Pharmaceuticals PLC', 'Antihistamine / এলার্জি', 'Square Pharmaceuticals PLC', 80, 25, 45.00, 70.00, '2026-11-30'),

            # Vitamins
            ('Vitamin C', 'Ascorbic Acid', 'Vitamin C', 'Tablet', '500 mg', 'Square Pharmaceuticals PLC', 'Vitamin & Supplement / ভিটামিন', 'Square Pharmaceuticals PLC', 400, 80, 2.00, 3.50, '2027-09-30'),
            ('A-Cal D', 'Calcium + Vitamin D3', 'A-Cal D', 'Tablet', '500 mg+200 IU', 'ACME Laboratories Ltd.', 'Vitamin & Supplement / ভিটামিন', 'ACME Laboratories Ltd.', 150, 40, 7.00, 12.00, '2027-08-31'),
            ('Neurobion', 'Vitamin B1+B6+B12', 'Neurobion', 'Tablet', '100 mg+200 mg+200 mcg', 'Opsonin Pharma Ltd.', 'Vitamin & Supplement / ভিটামিন', 'Opsonin Pharma Ltd.', 200, 50, 6.00, 10.00, '2027-05-31'),
            ('Zinca', 'Zinc Sulfate', 'Zinca', 'Syrup', '20 mg/5 ml', 'Square Pharmaceuticals PLC', 'Vitamin & Supplement / ভিটামিন', 'Square Pharmaceuticals PLC', 90, 30, 40.00, 65.00, '2026-12-31'),

            # Respiratory
            ('Sultolin', 'Salbutamol Sulphate', 'Sultolin', 'Inhaler', '100 mcg/dose', 'Square Pharmaceuticals PLC', 'Respiratory / শ্বাস-প্রশ্বাস', 'Square Pharmaceuticals PLC', 40, 15, 120.00, 185.00, '2026-10-31'),
            ('Montek', 'Montelukast Sodium', 'Montek', 'Tablet', '10 mg', 'Incepta Pharmaceuticals Ltd.', 'Respiratory / শ্বাস-প্রশ্বাস', 'Incepta Pharmaceuticals Ltd.', 80, 25, 18.00, 28.00, '2027-02-28'),
            ('Ambrox', 'Ambroxol HCl', 'Ambrox', 'Syrup', '15 mg/5 ml', 'Beximco Pharmaceuticals Ltd.', 'Respiratory / শ্বাস-প্রশ্বাস', 'Beximco Pharmaceuticals Ltd.', 100, 30, 35.00, 55.00, '2026-11-30'),

            # Cardiovascular / Statin
            ('Statin', 'Atorvastatin Calcium', 'Statin', 'Tablet', '20 mg', 'Square Pharmaceuticals PLC', 'Statin / কোলেস্টেরল', 'Square Pharmaceuticals PLC', 160, 40, 12.00, 20.00, '2027-06-30'),
            ('Lipovas', 'Rosuvastatin Calcium', 'Lipovas', 'Tablet', '10 mg', 'Square Pharmaceuticals PLC', 'Statin / কোলেস্টেরল', 'Square Pharmaceuticals PLC', 90, 30, 20.00, 32.00, '2027-04-30'),
            ('Clopid', 'Clopidogrel', 'Clopid', 'Tablet', '75 mg', 'Square Pharmaceuticals PLC', 'Cardiovascular / হৃদরোগ', 'Square Pharmaceuticals PLC', 8, 20, 18.00, 28.00, '2026-09-30'),

            # ORS & others
            ('SMECTA', 'Diosmectite', 'SMECTA', 'Powder', '3 g/sachet', 'Incepta Pharmaceuticals Ltd.', 'Gastrointestinal / পেটের ওষুধ', 'Incepta Pharmaceuticals Ltd.', 200, 50, 18.00, 28.00, '2027-08-31'),
            ('ORS', 'Oral Rehydration Salts', 'ORS', 'Powder', '27.9 g/sachet', 'Square Pharmaceuticals PLC', 'Oral Rehydration / স্যালাইন', 'Square Pharmaceuticals PLC', 500, 100, 5.00, 8.00, '2027-12-31'),
            ('Filmet', 'Metronidazole', 'Filmet', 'Tablet', '400 mg', 'Square Pharmaceuticals PLC', 'Antibiotic / এন্টিবায়োটিক', 'Square Pharmaceuticals PLC', 200, 50, 3.00, 5.00, '2027-10-31'),
            ('Flucon', 'Fluconazole', 'Flucon', 'Capsule', '150 mg', 'Square Pharmaceuticals PLC', 'Antifungal / ছত্রাকনাশক', 'Square Pharmaceuticals PLC', 60, 20, 28.00, 45.00, '2027-03-31'),
            ('Fusiderm', 'Fusidic Acid', 'Fusiderm', 'Cream', '2%', 'Square Pharmaceuticals PLC', 'Dermatology / চর্মরোগ', 'Square Pharmaceuticals PLC', 50, 15, 55.00, 85.00, '2026-12-31'),
        ]

        created = 0
        for (name, generic, brand, form, strength, mfr, cat_name, sup_name, stock, reorder, pp, sp, expiry) in medicines_data:
            cat = categories.get(cat_name)
            sup = suppliers.get(sup_name)
            _, c = Medicine.objects.get_or_create(
                name=name, strength=strength, dosage_form=form,
                defaults={
                    'generic_name': generic,
                    'brand_name': brand,
                    'manufacturer': mfr,
                    'category': cat,
                    'supplier': sup,
                    'stock_quantity': stock,
                    'reorder_level': reorder,
                    'purchase_price': Decimal(str(pp)),
                    'selling_price': Decimal(str(sp)),
                    'expiry_date': expiry,
                }
            )
            if c:
                created += 1

        self.stdout.write(f'  ✓ {created} medicines seeded (from medex.com.bd brands)')

        # ── Sample Customers ───────────────────────────────────────────────────
        customers_data = [
            ('মোঃ রহিম উদ্দিন', '01711-123456', '', 'চৌমুহনা, মৌলভীবাজার', '1970-03-15'),
            ('ফাতেমা বেগম', '01812-234567', '', 'কমলগঞ্জ, মৌলভীবাজার', '1985-07-22'),
            ('আবুল কালাম', '01913-345678', '', 'শ্রীমঙ্গল, মৌলভীবাজার', '1960-11-10'),
            ('সুমাইয়া আক্তার', '01615-456789', '', 'রাজনগর, মৌলভীবাজার', '1995-02-28'),
            ('মোঃ করিম মিয়া', '01516-567890', '', 'বড়লেখা, মৌলভীবাজার', '1975-09-05'),
        ]
        for name, phone, email, address, dob in customers_data:
            Customer.objects.get_or_create(name=name, defaults={
                'phone': phone, 'email': email, 'address': address, 'date_of_birth': dob,
            })
        self.stdout.write(f'  ✓ {len(customers_data)} sample customers added')

        self.stdout.write(self.style.SUCCESS('\n  ✅ পল মেডিকো — সেটআপ সম্পন্ন!\n'))
        self.stdout.write('  লগইন তথ্য:')
        self.stdout.write('    Admin  → admin   / admin123')
        self.stdout.write('    Staff  → staff   / staff123')
        self.stdout.write('\n  সার্ভার চালু করুন: python manage.py runserver\n')
