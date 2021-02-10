import datetime
import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from smsApp.models import CustomUser, Courses, Staffs, Subjects, Students, SessionYear, FeedBackStaff, FeedBackStudent, \
    LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport


def admin_dashboard(request):
    student_count = Students.objects.all().count()
    staff_count = Staffs.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()

    courses = Courses.objects.all()
    course_name = []
    student_list = []
    subject_list = []
    for course in courses:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        course_name.append(course.course_name)
        student_list.append(students)
        subject_list.append(subjects)

    subjects = Subjects.objects.all()
    subject_name = []
    student_list_subject = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        student_subject = Students.objects.filter(course_id=course.id).count()
        subject_name.append(subject.subject_name)
        student_list_subject.append(student_subject)

    staffs = Staffs.objects.all()
    attendance_attend_list = []
    attendance_leave_list = []
    staff_name_list = []
    for staff in staffs:
        subjects_id = Subjects.objects.filter(staff_id=staff.admin.id)
        attends = Attendance.objects.filter(subject_id__in=subjects_id).count()
        leaves = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
        attendance_attend_list.append(attends)
        attendance_leave_list.append(leaves)
        staff_name_list.append(staff.admin.username)

    # Count student attend
    students_attendance = Students.objects.all()
    student_list2 = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        attendance_absent_count = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
        student_list2.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count+leaves)

    context = {
        'page_tittle': 'Admin Dashboard',
        'student_count': student_count,
        'staff_count': staff_count,
        'course_count': course_count,
        'subject_count': subject_count,
        'course_name': course_name,
        'subject_list': subject_list,
        'student_list': student_list,
        'subject_name': subject_name,
        'student_list_subject': student_list_subject,
        'attend': attendance_attend_list,
        'leave': attendance_leave_list,
        'staff_name_list': staff_name_list,
        'student_list2': student_list2,
        'student_attend': student_list_attendance_present,
        'student_absent': student_list_attendance_absent,
    }
    return render(request, 'base/page_content.html', context)

def admin_add_staff(request):
    context = {
        'page_tittle':'Add Staff'
    }
    return render(request, 'base/add_staff.html', context)

def admin_add_staff_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, 'Staff added successfully!')
            return HttpResponseRedirect('/admin_add_staff')
        except:
            messages.error(request, 'Staff failed to add!')
            return HttpResponseRedirect('/admin_add_staff')

def admin_add_course(request):
    context = {
        'page_tittle':'Add course'
    }
    return render(request, 'base/add_course.html', context)

def admin_add_course_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        course_name = request.POST.get('course_name')
        try:
            course = Courses(course_name=course_name)
            course.save()
            messages.success(request, 'Course added successfully!')
            return HttpResponseRedirect('/admin_add_course')
        except:
            messages.error(request, 'Course failed to add!')
            return HttpResponseRedirect('/admin_add_course')

def admin_add_student(request):
    courses = Courses.objects.all()
    sessions = SessionYear.objects.all()
    context = {
        'page_tittle':'Add student',
        'courses':courses,
        'sessions':sessions
    }
    return render(request, 'base/add_student.html', context)

def admin_add_student_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course')
        session_id = request.POST.get('session')

        profile_picture = request.FILES['profile_picture']
        fs = FileSystemStorage()
        filename = fs.save(profile_picture.name, profile_picture)
        profile_picture_url = fs.url(filename)
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            user.students.gender = gender
            user.students.address = address
            user.students.profile_picture = profile_picture_url
            course_obj = Courses.objects.get(id=course_id)
            user.students.course_id_id = course_obj
            session_obj = SessionYear.objects.get(id=session_id)
            user.students.session_year_id_id = session_obj
            user.save()
            messages.success(request, 'Student added successfully!')
            return HttpResponseRedirect('/admin_add_student')
        except:
            messages.error(request, 'Student failed to add!')
            return HttpResponseRedirect('/admin_add_student')

def admin_add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    context = {
        'page_tittle':'Add subject',
        'courses':courses,
        'staffs':staffs
    }
    return render(request, 'base/add_subject.html', context)

def admin_add_subject_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)
        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, 'Subject added successfully!')
            return HttpResponseRedirect('/admin_add_subject')
        except:
            messages.error(request, 'Subject failed to add!')
            return HttpResponseRedirect('/admin_add_subject')

def admin_manage_staff(request):
    staffs = Staffs.objects.all()
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 5))
    paginator = Paginator(staffs, per_page)
    page_object = paginator.page(page)
    context = {
        'page_tittle':'Manage staff',
        'staffs':page_object,
        'page': paginator.page_range,
    }
    return render(request, 'base/manage_staff.html', context)

def admin_manage_student(request):
    students = Students.objects.all()
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 5))
    paginator = Paginator(students, per_page)
    page_object = paginator.page(page)
    context = {
        'page_tittle':'Manage student',
        'students':page_object,
        'page': paginator.page_range,
    }
    return render(request, 'base/manage_student.html', context)

def admin_manage_course(request):
    courses = Courses.objects.all()
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 5))
    paginator = Paginator(courses, per_page)
    page_object = paginator.page(page)
    context = {
        'page_tittle':'Manage course',
        'courses':page_object,
        'page': paginator.page_range,
    }
    return render(request, 'base/manage_course.html', context)

def admin_manage_subject(request):
    subjects = Subjects.objects.all()
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 5))
    paginator = Paginator(subjects, per_page)
    page_object = paginator.page(page)
    context = {
        'page_tittle':'Manage subject',
        'subjects':page_object,
        'page': paginator.page_range,
    }
    return render(request, 'base/manage_subject.html', context)

def admin_edit_staff(request, staff_id):
    staffs = Staffs.objects.get(admin=staff_id)
    context = {
        'page_tittle':'Edit staff',
        'staffs':staffs
    }
    return render(request, 'base/edit_staff.html', context)

def admin_edit_staff_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()
            messages.success(request, 'Staff edited successfully!')
            return HttpResponseRedirect('/admin_edit_staff/'+staff_id)
        except:
            messages.error(request, 'Staff failed to edit!')
            return HttpResponseRedirect('/admin_edit_staff/'+staff_id)

def admin_edit_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    courses = Courses.objects.all()
    sessions = SessionYear.objects.all()
    context = {
        'page_tittle':'Edit student',
        'student':student,
        'courses':courses,
        'sessions':sessions
    }
    return render(request, 'base/edit_student.html', context)

def admin_edit_student_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        student_id = request.POST.get('student_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course')
        session_id = request.POST.get('session')

        if request.FILES.get('profile_picture', False):
            profile_picture = request.FILES['profile_picture']
            fs = FileSystemStorage()
            filename = fs.save(profile_picture.name, profile_picture)
            profile_picture_url = fs.url(filename)
        else:
            profile_picture_url = None

        try:
            user = CustomUser.objects.get(id=student_id)
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            student = Students.objects.get(admin=student_id)
            student.address = address
            student.gender = gender

            if profile_picture_url != None:
                student.profile_picture = profile_picture_url
            course_obj = Courses.objects.get(id=course_id)
            student.course_id = course_obj
            session_obj = SessionYear.objects.get(id=session_id)
            student.session_id = session_obj
            student.save()

            messages.success(request, 'Student edited successfully!')
            return HttpResponseRedirect('/admin_edit_student/'+student_id)
        except:
            messages.error(request, 'Student failed to edit!')
            return HttpResponseRedirect('/admin_edit_student/'+student_id)

def admin_edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    context = {
        'page_tittle':'Edit course',
        'course':course
    }
    return render(request, 'base/edit_course.html', context)

def admin_edit_course_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        course_name = request.POST.get('course_name')
        course_id = request.POST.get('course_id')
        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, 'Course edited successfully!')
            return HttpResponseRedirect('/admin_edit_course/'+course_id)
        except:
            messages.error(request, 'Course failed to edit!')
            return HttpResponseRedirect('/admin_edit_course/'+course_id)

def admin_edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    context = {
        'page_tittle':'Edit subject',
        'courses':courses,
        'staffs':staffs,
        'subject':subject
    }
    return render(request, 'base/edit_subject.html', context)

def admin_edit_subject_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        subject_name = request.POST.get('subject_name')
        subject_id = request.POST.get('subject_id')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')
        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            subject.save()

            messages.success(request, 'Subject edited successfully!')
            return HttpResponseRedirect('/admin_edit_subject/'+subject_id)
        except:
            messages.error(request, 'Subject failed to edit!')
            return HttpResponseRedirect('/admin_edit_subject/'+subject_id)

def admin_manage_session_year(request):
    sessions_year = SessionYear.objects.all()
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 5))
    paginator = Paginator(sessions_year, per_page)
    page_object = paginator.page(page)
    context = {
        'page_tittle':'Manage session year',
        'sessions_year':page_object,
        'page':paginator.page_range,
    }
    return render(request, 'base/manage_session_year.html', context)

def admin_add_session_year(request):
    context = {
        'page_tittle':'Add session year',
    }
    return render(request, 'base/add_session_year.html', context)

def admin_add_session_year_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')
        try:
            session_year = SessionYear(session_start_year=session_start_year, session_end_year=session_end_year)
            session_year.save()

            messages.success(request, 'Session year add successfully!')
            return HttpResponseRedirect('/admin_add_session_year')
        except:
            messages.error(request, 'Session year failed to add!')
            return HttpResponseRedirect('/admin_add_session_year')

def admin_edit_session_year(request, session_id):
    session_year = SessionYear.objects.get(id=session_id)
    context = {
        'page_tittle':'Edit session year',
        'session':session_year
    }
    return render(request, 'base/edit_session_year.html', context)

def admin_edit_session_year_save(request):
    if request.method != 'POST':
        return HttpResponse('Not Allowed!')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')
        session_id = request.POST.get('session_id')
        try:
            session_year = SessionYear.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()

            messages.success(request, 'Session year edited successfully!')
            return HttpResponseRedirect('/admin_edit_session_year/'+session_id)
        except:
            messages.error(request, 'Session year failed to edit!')
            return HttpResponseRedirect('/admin_edit_session_year/'+session_id)

def admin_feedback_staff(request):
    feedbacks = FeedBackStaff.objects.all()
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 5))
    paginator = Paginator(feedbacks, per_page)
    page_object = paginator.page(page)
    context = {
        'page_tittle':'Staff feedback',
        'feedbacks':page_object,
        'page':paginator.page_range,
    }
    return render(request, 'base/staff_feedback.html', context)

def admin_feedback_student(request):
    feedbacks = FeedBackStudent.objects.all()
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 5))
    paginator = Paginator(feedbacks, per_page)
    page_object = paginator.page(page)
    context = {
        'page_tittle': 'Student feedback',
        'feedbacks': page_object,
        'page': paginator.page_range,
    }
    return render(request, 'base/student_feedback.html', context)

@csrf_exempt
def admin_feedback_staff_reply(request):
    feedback_id = request.POST.get('id')
    feedback_message = request.POST.get('message')

    try:
        feedback = FeedBackStaff.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse('True')
    except:
        return HttpResponse('False')

@csrf_exempt
def admin_feedback_student_reply(request):
    student_id = request.POST.get('id')
    feedback_message = request.POST.get('message')

    try:
        feedback = FeedBackStudent.objects.get(id=student_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse('True')
    except:
        return HttpResponse('False')

def admin_leave_student(request):
    leaves = LeaveReportStudent.objects.all()
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 5))
    paginator = Paginator(leaves, per_page)
    page_object = paginator.page(page)
    context = {
        'page_tittle':'Leave student',
        'leaves':page_object,
        'page':paginator.page_range,
    }
    return render(request, 'base/leave_student.html', context)

def admin_leave_staff(request):
    leaves = LeaveReportStaff.objects.all()
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 5))
    paginator = Paginator(leaves, per_page)
    page_object = paginator.page(page)
    context = {
        'page_tittle': 'Leave staff',
        'leaves': page_object,
        'page': paginator.page_range,
    }
    return render(request, 'base/leave_staff.html', context)

def admin_leave_student_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect('/admin_leave_student')

def admin_leave_student_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect('/admin_leave_student')

def admin_leave_staff_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect('/admin_leave_staff')

def admin_leave_staff_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect('/admin_leave_staff')

def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_year = SessionYear.objects.all()
    context = {
        'page_tittle': 'View attendance',
        'subjects': subjects,
        'session_year_id': session_year
    }
    return render(request, 'base/view_attendance.html', context)

@csrf_exempt
def admin_get_attendance_dates(request):
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
def admin_get_attendance_students(request):
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