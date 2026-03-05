from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('dashboard/'), name='home'),
    path('admin/', admin.site.urls),
    path('', include('pharmacy.urls')),
    path('api/', include('pharmacy.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "পল মেডিকো — Administration"
admin.site.site_title = "POL MEDICO Admin"
admin.site.index_title = "Pharmacy Management — মৌলভীবাজার"
