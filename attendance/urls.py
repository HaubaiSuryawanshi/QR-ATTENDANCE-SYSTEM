from django.urls import path
from . import views

urlpatterns = [

    # Admin Dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # camera scanner page
    path('scan/', views.scan_page, name='scan_page'),

    # QR scan hone ke baad attendance mark karega
    path('mark-attendance/', views.scan_attendance, name='scan_attendance'),


    
    path("student/<int:id>/", views.student_profile),


]
