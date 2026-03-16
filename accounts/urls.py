from django.urls import path
from . import views

urlpatterns = [

path('',views.login_view,name='login'),

path('register/',views.register,name='register'),

path('dashboard/',views.dashboard,name='dashboard'),

# PDF download URL
path('attendance-pdf/',views.attendance_pdf,name='attendance_pdf'),

]