#!/bin/bash
# ═══════════════════════════════════════════════════
#   POL MEDICO — পল মেডিকো
#   সেটআপ স্ক্রিপ্ট
# ═══════════════════════════════════════════════════

echo ""
echo "  💊  POL MEDICO — পল মেডিকো"
echo "  কোর্ট রোড, চৌমুহনা, মৌলভীবাজার"
echo "  ═══════════════════════════════════════"
echo ""

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic --noinput 2>/dev/null

echo ""
echo "  ✅ সেটআপ সম্পন্ন!"
echo ""
echo "  চালু করুন:"
echo "    python manage.py runserver"
echo ""
echo "  তারপর খুলুন: http://127.0.0.1:8000"
echo ""
echo "  লগইন:"
echo "    admin  →  admin123"
echo "    staff  →  staff123"
echo ""
