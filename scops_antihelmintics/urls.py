"""
scops_antihelmintics URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('drug_database.urls')),
    path('admin/', admin.site.urls),
]

# Admin site conf
admin.site.site_title = 'SCOPS Antih. Admin'
admin.site.site_header = 'SCOPS Antihelmintics Administration Site'
