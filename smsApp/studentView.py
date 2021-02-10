import datetime

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from smsApp.models import Students, Courses, Subjects, CustomUser, Attendance, AttendanceReport, LeaveReportStudent, \
    FeedBackStudent, StudentResult


def student_dashboard(request):
    student_obj = Students.objects.get(admin=request.user.id)
    attendance_total = AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status=False).count()
    course = Courses.objects.get(id=student_obj.course_id.id)
    subjects = Subjects.objects.filter(course_id=course).count()
    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=student_obj, status=True).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=student_obj, status=False).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    context = {
        'page_tittle':'Student dashboard',
        'attendance_total':attendance_total,
        'attendance_present':attendance_present,
        'attendance_absent':attendance_absent,
        'subjects':subjects,
        'subject_name':subject_name,
        'data_present':data_present,
        'data_absent':data_absent,
        'student':student_obj,
    }
    return render(request, 'student_template/page_content.html', context)

def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id)
    course = Courses.objects.get(id=student.course_id.id)
    subjects = Subjects.objects.filter(course_id=course)

    context = {
        'page_tittle':'View attendance',
        'subjects':subjects,
        'student': student,
    }
    return render(request, 'student_template/view_attendance.html', context)

def student_view_attendance_post(request):
    subject_id = request.POST.get('subject')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    subject_obj = Subjects.objects.get(id=subject_id)
    user_obj = CustomUser.objects.get(id=request.user.id)
    student_obj = Students.objects.get(admin=user_obj)

    attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse,end_date_parse), subject_id=subject_obj)
    attendance_report = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=student_obj)

    context ={
        'page_tittle':'View attendance',
        'attendance_report':attendance_report,
        'student': student_obj,
    }

    return render(request, 'student_template/attendance_date.html', context)

def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_report = LeaveReportStudent.objects.filter(student_id=student_obj)
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 4))
    paginator = Paginator(leave_report, per_page)
    page_object = paginator.page(page)
    context = {
        'page_tittle':'Apply leave',
        'leaves':page_object,
        'page': paginator.page_range,
        'student': student_obj,
    }
    return render(request, 'student_template/apply_leave.html', context)

def student_apply_leave_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        leave_date = request.POST.get('leave_date')
        leave_reason = request.POST.get('leave_reason')
        try:
            student_obj = Students.objects.get(admin=request.user.id)
            leave_report = LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_reason, leave_status=0)
            leave_report.save()

            messages.success(request, 'Apply leave successfully!')
            return HttpResponseRedirect('/student_apply_leave')
        except:
            messages.error(request, 'Apply leave failed!')
            return HttpResponseRedirect('/student_apply_leave')

def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedbacks = FeedBackStudent.objects.filter(student_id=student_obj)
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 4))
    paginator = Paginator(feedbacks, per_page)
    page_object = paginator.page(page)
    context = {
        'page_tittle': 'Feedback',
        'feedbacks':page_object,
        'page':paginator.page_range,
        'student':student_obj,
    }
    return render(request, 'student_template/feedback.html', context)

def student_feedback_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        feedback = request.POST.get('feedback')
        try:
            student_obj = Students.objects.get(admin=request.user.id)
            feedback_model = FeedBackStudent(student_id=student_obj, feedback=feedback, feedback_reply='')
            feedback_model.save()

            messages.success(request, 'Apply feedback successfully!')
            return HttpResponseRedirect('/student_feedback')
        except:
            messages.error(request, 'Apply feedback failed!')
            return HttpResponseRedirect('/student_feedback')

def student_view_result(request):
    student = Students.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student.id)
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 4))
    paginator = Paginator(student_result, per_page)
    page_object = paginator.page(page)
    context = {
        'page_tittle': 'View result',
        'student_result': page_object,
        'page': paginator.page_range,
        'student': student,
    }
    return render(request, 'student_template/view_result.html', context)