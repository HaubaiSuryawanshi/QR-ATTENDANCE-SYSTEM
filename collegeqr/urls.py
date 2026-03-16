from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from attendance import views as attendance_views
from accounts import views as account_views

urlpatterns = [

    # Django Admin panel
    path('admin/', admin.site.urls),

    # Student system (register, login, dashboard)
    path('', include('accounts.urls')),

    # Attendance APIs
    path('', include('attendance.urls')),

    # Admin Dashboard
    path('admin-dashboard/', account_views.admin_dashboard, name='admin_dashboard'),

    # QR Scanner page for admin
    path('scan/', attendance_views.scan_page, name='scan_page'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
