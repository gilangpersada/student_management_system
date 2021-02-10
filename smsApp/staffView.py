import json

from django.contrib import messages
from django.core import serializers
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from smsApp.models import Subjects, SessionYear, Students, Attendance, AttendanceReport, LeaveReportStaff, Staffs, \
    FeedBackStaff, Courses, StudentResult


def staff_dashboard(request):
    #Count student
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course)

    final_course = []
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count = Students.objects.filter(course_id__in=final_course).count()

    #Count attendance
    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()

    #Count leave taken
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(staff_id=staff_obj.id, leave_status=1).count()

    #Count subject
    subject_count = subjects.count()

    #Count attend of its subject
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count2 = Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count2)

    #Count student attend
    students_attendance = Students.objects.filter(course_id__in=final_course)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        attendance_absent_count = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    context = {
        'page_tittle':'Staff dashboard',
        'students_count':students_count,
        'attendance_count':attendance_count,
        'leave_count':leave_count,
        'subject_count':subject_count,
        'subject_list':subject_list,
        'attendance_list':attendance_list,
        'student_list':student_list,
        'present_list':student_list_attendance_present,
        'absent_list':student_list_attendance_absent,
    }
    return render(request, 'staff_template/page_content.html', context)

def staff_take_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYear.objects.all()
    context = {
        'page_tittle':'Take attendance',
        'session_years':session_years,
        'subjects':subjects
    }
    return render(request, 'staff_template/take_attendance.html', context)

@csrf_exempt
def staff_get_students(request):
    subject_id = request.POST.get('subject')
    session_year = request.POST.get('session_year')

    try:
        subject = Subjects.objects.get(id=subject_id)
        session_model = SessionYear.objects.get(id=session_year)
        students = Students.objects.filter(course_id=subject.course_id, session_year_id=session_model)

        list_data = []
        for student in students:
            data = {
                'id':student.admin.id,
                'name':student.admin.first_name+ " " + student.admin.last_name,
            }

            list_data.append(data)
        return JsonResponse(json.dumps(list_data), content_type='application/json', safe=False)

    except:
        return HttpResponse('error')

@csrf_exempt
def staff_attendance_data_save(request):
    students_id = request.POST.get('students_id')
    subject_id = request.POST.get('subject_id')
    attendance_date = request.POST.get('attendance_date')
    session_year_id = request.POST.get('session_year_id')

    try:
        subject_model = Subjects.objects.get(id=subject_id)
        session_model = SessionYear.objects.get(id=session_year_id)
        attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date, session_year_id=session_model)
        attendance.save()
        json_sstudent = json.loads(students_id)

        for stud in json_sstudent:
            student = Students.objects.get(admin=stud['id'])
            print(stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()

        return HttpResponse('ok')
    except:
        return HttpResponse('error')

def staff_update_attendance_data(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_year = SessionYear.objects.all()
    context = {
        'page_tittle':'Update attendance',
        'subjects':subjects,
        'session_year_id':session_year
    }
    return render(request, 'staff_template/update_attendance.html', context)

@csrf_exempt
def staff_get_attendance_dates(request):
    subject_id = request.POST.get('subject_id')
    session_year_id = request.POST.get('session_year_id')
    subject_obj = Subjects.objects.get(id=subject_id)
    session_year_obj = SessionYear.objects.get(id=session_year_id)
    attendance = Attendance.objects.filter(subject_id=subject_obj, session_year_id=session_year_obj)
    attendance_obj = []

    for attendance_single in attendance:
        data = {
            'id':attendance_single.id,
            'attendance_date':str(attendance_single.attendance_date),
            'sesssion_year_id':attendance_single.session_year_id.id,
        }
        attendance_obj.append(data)
    return JsonResponse(json.dumps(attendance_obj), content_type='application/json', safe=False)

@csrf_exempt
def staff_get_attendance_students(request):
    attendance_date_id = request.POST.get('attendance_date')

    try:
        attendance = Attendance.objects.get(id=attendance_date_id)
        attendance_obj = AttendanceReport.objects.filter(attendance_id=attendance)

        list_data = []
        for student in attendance_obj:
            data = {
                'id': student.student_id.admin.id,
                'name': student.student_id.admin.first_name + " " + student.student_id.admin.last_name,
                'status':student.status
            }

            list_data.append(data)
        return JsonResponse(json.dumps(list_data), content_type='application/json', safe=False)

    except:
        return HttpResponse('error')

@csrf_exempt
def staff_update_attendance_data_save(request):
    students_id = request.POST.get('students_id')
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    try:
        json_sstudent = json.loads(students_id)
        for stud in json_sstudent:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status = stud['status']
            attendance_report.save()

        return HttpResponse('ok')
    except:
        return HttpResponse('error')

def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_report = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 4))
    paginator = Paginator(leave_report, per_page)
    page_object = paginator.page(page)
    context = {
        'page_tittle':'Apply leave',
        'leaves':page_object,
        'page': paginator.page_range,
    }
    return render(request, 'staff_template/apply_leave.html', context)

def staff_apply_leave_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        leave_date = request.POST.get('leave_date')
        leave_reason = request.POST.get('leave_reason')
        try:
            staff_obj = Staffs.objects.get(admin=request.user.id)
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_reason, leave_status=0)
            leave_report.save()

            messages.success(request, 'Apply leave successfully!')
            return HttpResponseRedirect('/staff_apply_leave')
        except:
            messages.error(request, 'Apply leave failed!')
            return HttpResponseRedirect('/staff_apply_leave')

def staff_feedback(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    feedbacks = FeedBackStaff.objects.filter(staff_id=staff_obj)
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 4))
    paginator = Paginator(feedbacks, per_page)
    page_object = paginator.page(page)
    context = {
        'page_tittle': 'Feedback',
        'feedbacks':page_object,
        'page': paginator.page_range,
    }
    return render(request, 'staff_template/feedback.html', context)

def staff_feedback_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        feedback = request.POST.get('feedback')
        try:
            staff_obj = Staffs.objects.get(admin=request.user.id)
            feedback_model = FeedBackStaff(staff_id=staff_obj, feedback=feedback, feedback_reply='')
            feedback_model.save()

            messages.success(request, 'Apply feedback successfully!')
            return HttpResponseRedirect('/staff_feedback')
        except:
            messages.error(request, 'Apply feedback failed!')
            return HttpResponseRedirect('/staff_feedback')

def staff_add_result(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYear.objects.all()
    context = {
        'page_tittle': 'Add result',
        'subjects': subjects,
        'session_years': session_years,
    }
    return render(request, 'staff_template/add_result.html', context)

def staff_add_result_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        student_admin_id = request.POST.get('student_list')
        assignment_marks = request.POST.get('assignment_marks')
        exam_marks = request.POST.get('exam_marks')
        subject_id = request.POST.get('subject')
        print(student_admin_id)
        print(assignment_marks)
        print(exam_marks)
        print(subject_id)

        student_obj = Students.objects.get(admin=student_admin_id)
        subject_obj = Subjects.objects.get(id=subject_id)

        try:
            check_exist = StudentResult.objects.filter(subject_id=subject_obj, student_id=student_obj).exists()
            if check_exist:
                result = StudentResult.objects.get(subject_id=subject_obj, student_id=student_obj)
                result.subject_assignment_marks = assignment_marks
                result.subject_exam_marks = exam_marks
                result.save()

                messages.success(request, 'Add result updated successfully!')
                return HttpResponseRedirect('/staff_add_result')
            else:
                result = StudentResult(student_id=student_obj, subject_id=subject_obj, subject_exam_marks=exam_marks, subject_assignment_marks=assignment_marks)
                result.save()

                messages.success(request, 'Add result successfully!')
                return HttpResponseRedirect('/staff_add_result')

        except:
            messages.error(request, 'Add result failed!')
            return HttpResponseRedirect('/staff_add_result')