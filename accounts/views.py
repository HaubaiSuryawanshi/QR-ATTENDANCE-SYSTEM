from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import StudentProfile
import qrcode
from django.conf import settings
import os

# PDF library
from reportlab.pdfgen import canvas
from datetime import date


def generate_qr(profile):

    data = profile.roll_no
    img = qrcode.make(data)

    qr_dir = os.path.join(settings.MEDIA_ROOT,'qr_codes')
    os.makedirs(qr_dir,exist_ok=True)

    path = os.path.join(qr_dir,f"{profile.roll_no}.png")

    img.save(path)

    profile.qr_code = f"qr_codes/{profile.roll_no}.png"
    profile.save()


def register(request):

    if request.method=='POST':

        username=request.POST['username']
        password=request.POST['password']
        name=request.POST['student_name']
        roll=request.POST['roll']
        dept=request.POST['department']
        student_class=request.POST['student_class']
        email=request.POST['email']
        photo=request.FILES.get('photo')

        user=User.objects.create_user(
            username=username,
            password=password
        )

        profile=StudentProfile.objects.create(
            user=user,
            student_name=name,
            roll_no=roll,
            department=dept,
            student_class=student_class,
            email=email,
            photo=photo
        )

        generate_qr(profile)

        return redirect('login')

    return render(request,'accounts/register.html')


def login_view(request):

    if request.method=='POST':

        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)

        if user:

            login(request,user)

            # ADMIN LOGIN
            if user.is_superuser:
                return redirect('admin_dashboard')

            # STUDENT LOGIN
            else:
                return redirect('dashboard')

    return render(request,'accounts/login.html')


@login_required
def dashboard(request):

    student, created = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "roll_no": request.user.username
        }
    )

    if not student.qr_code:
        generate_qr(student)

    from attendance.models import Attendance

    attendance = Attendance.objects.filter(student=student)

    present = attendance.filter(status="Present").count()
    total = attendance.count()
    absent = total - present

    return render(request,'accounts/dashboard.html',{
        'student':student,
        'attendance':attendance,
        'present':present,
        'absent':absent
    })


# 🔥 ADMIN DASHBOARD
@login_required
def admin_dashboard(request):

    from attendance.models import Attendance
    from .models import StudentProfile

    students = StudentProfile.objects.all()

    attendance = Attendance.objects.select_related('student').order_by('-date','-time')

    return render(request,'accounts/admin_dashboard.html',{
        'students':students,
        'attendance':attendance
    })


# 🔥 DOWNLOAD ATTENDANCE PDF
@login_required
def attendance_pdf(request):

    from attendance.models import Attendance

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica",16)
    p.drawString(200,800,"QR Attendance Report")

    p.setFont("Helvetica",12)

    today = date.today()

    attendance = Attendance.objects.filter(date=today)

    y = 760

    for a in attendance:

        line = f"{a.student.student_name} | Roll: {a.student.roll_no} | {a.status}"

        p.drawString(50,y,line)

        y -= 20

    p.showPage()
    p.save()

    return response