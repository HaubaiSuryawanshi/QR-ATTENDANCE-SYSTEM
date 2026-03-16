from django.http import JsonResponse
from datetime import date
from accounts.models import StudentProfile
from .models import Attendance
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import json


# ==============================
# QR SCAN ATTENDANCE
# ==============================

@csrf_exempt
def scan_attendance(request):

    if request.method == "POST":

        try:
            data = json.loads(request.body)
            roll = data.get('qr_data')
            subject = data.get('subject', 'General')
        except:
            roll = request.POST.get('roll')
            subject = request.POST.get('subject')

        if not roll:
            return JsonResponse({
                'status': 'Invalid QR Code'
            })

        try:
            student = StudentProfile.objects.get(roll_no=roll)
        except StudentProfile.DoesNotExist:
            return JsonResponse({
                'status': 'Student Not Found'
            })

        today = date.today()

        # Duplicate Check
        already_marked = Attendance.objects.filter(
            student=student,
            subject=subject,
            date=today
        ).exists()

        # Stats
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status="Present").count()
        absent = total - present

        photo = ""
        if student.photo:
            photo = student.photo.url

        if already_marked:
            return JsonResponse({
                'status': 'Already Marked',
                'name': student.student_name,
                'roll': student.roll_no,
                'class': student.student_class,
                'dept': student.department,
                'photo': photo,
                'present': present,
                'absent': absent
            })

        # Create attendance
        Attendance.objects.create(
            student=student,
            subject=subject,
            status="Present",
            date=today
        )

        return JsonResponse({
            'status': 'Attendance Marked',
            'name': student.student_name,
            'roll': student.roll_no,
            'class': student.student_class,
            'dept': student.department,
            'photo': photo,
            'present': present + 1,
            'absent': absent
        })


# ==============================
# SCANNER PAGE
# ==============================

@login_required
def scan_page(request):

    if not request.user.is_staff:
        return redirect('/dashboard')

    return render(request, 'attendance/scan.html')


# ==============================
# ADMIN DASHBOARD
# ==============================

@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect('/dashboard')

    total_students = StudentProfile.objects.count()

    today_attendance = Attendance.objects.filter(
        date=date.today()
    ).count()

    present = Attendance.objects.filter(
        status="Present",
        date=date.today()
    ).count()

    absent = total_students - present

    attendance_list = Attendance.objects.select_related('student').order_by('-date')

    # Chart Data
    chart_data = Attendance.objects.values('date').annotate(count=Count('id')).order_by('date')

    labels = []
    counts = []

    for data in chart_data:
        labels.append(str(data['date']))
        counts.append(data['count'])

    return render(request, 'attendance/admin_dashboard.html', {
        'total_students': total_students,
        'today_attendance': today_attendance,
        'present': present,
        'absent': absent,
        'labels': labels,
        'counts': counts,
        'attendance_list': attendance_list
    })


# ==============================
# STUDENT PROFILE + FULL ATTENDANCE
# ==============================

@login_required
def student_profile(request, id):

    student = get_object_or_404(StudentProfile, id=id)

    attendance = Attendance.objects.filter(
        student=student
    ).order_by('-date')

    total = attendance.count()

    present = attendance.filter(status="Present").count()

    absent = total - present

    return render(request, "attendance/student_profile.html", {

        "student": student,
        "attendance": attendance,
        "total": total,
        "present": present,
        "absent": absent

    })