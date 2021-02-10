from django.urls import path, include

from . import views, adminView, staffView, studentView

urlpatterns = [
	path('', views.showLogin, name="showLogin"),
	path('userLogin', views.userLogin, name="userLogin"),
	path('userLogout', views.userLogout, name="userLogout"),

	path('admin_dashboard', adminView.admin_dashboard, name="admin_dashboard"),
	path('admin_add_staff', adminView.admin_add_staff, name="admin_add_staff"),
	path('admin_add_staff_save', adminView.admin_add_staff_save, name="admin_add_staff_save"),
	path('admin_add_course', adminView.admin_add_course, name="admin_add_course"),
	path('admin_add_course_save', adminView.admin_add_course_save, name="admin_add_course_save"),
	path('admin_add_student', adminView.admin_add_student, name="admin_add_student"),
	path('admin_add_student_save', adminView.admin_add_student_save, name="admin_add_student_save"),
	path('admin_add_subject', adminView.admin_add_subject, name="admin_add_subject"),
	path('admin_add_subject_save', adminView.admin_add_subject_save, name="admin_add_subject_save"),
	path('admin_add_session_year', adminView.admin_add_session_year, name="admin_add_session_year"),
	path('admin_add_session_year_save', adminView.admin_add_session_year_save, name="admin_add_session_year_save"),
	path('admin_manage_staff', adminView.admin_manage_staff, name="admin_manage_staff"),
	path('admin_manage_student', adminView.admin_manage_student, name="admin_manage_student"),
	path('admin_manage_course', adminView.admin_manage_course, name="admin_manage_course"),
	path('admin_manage_subject', adminView.admin_manage_subject, name="admin_manage_subject"),
	path('admin_manage_session_year', adminView.admin_manage_session_year, name="admin_manage_session_year"),
	path('admin_edit_staff/<str:staff_id>', adminView.admin_edit_staff, name="admin_edit_staff"),
	path('admin_edit_staff_save', adminView.admin_edit_staff_save, name="admin_edit_staff_save"),
	path('admin_edit_student/<str:student_id>', adminView.admin_edit_student, name="admin_edit_student"),
	path('admin_edit_student_save', adminView.admin_edit_student_save, name="admin_edit_student_save"),
	path('admin_edit_course/<str:course_id>', adminView.admin_edit_course, name="admin_edit_course"),
	path('admin_edit_course_save', adminView.admin_edit_course_save, name="admin_edit_course_save"),
	path('admin_edit_subject/<str:subject_id>', adminView.admin_edit_subject, name="admin_edit_subject"),
	path('admin_edit_subject_save', adminView.admin_edit_subject_save, name="admin_edit_subject_save"),
	path('admin_edit_session_year/<str:session_id>', adminView.admin_edit_session_year, name="admin_edit_session_year"),
	path('admin_edit_session_year_save', adminView.admin_edit_session_year_save, name="admin_edit_session_year_save"),
	path('admin_feedback_student', adminView.admin_feedback_student, name="admin_feedback_student"),
	path('admin_feedback_staff', adminView.admin_feedback_staff, name="admin_feedback_staff"),
	path('admin_feedback_staff_reply', adminView.admin_feedback_staff_reply, name="admin_feedback_staff_reply"),
	path('admin_feedback_student_reply', adminView.admin_feedback_student_reply, name="admin_feedback_student_reply"),
	path('admin_leave_student', adminView.admin_leave_student, name="admin_leave_student"),
	path('admin_leave_staff', adminView.admin_leave_staff, name="admin_leave_staff"),
	path('admin_leave_student_approve/<str:leave_id>', adminView.admin_leave_student_approve, name="admin_leave_student_approve"),
	path('admin_leave_student_reject/<str:leave_id>', adminView.admin_leave_student_reject, name="admin_leave_student_reject"),
	path('admin_leave_staff_approve/<str:leave_id>', adminView.admin_leave_staff_approve, name="admin_leave_staff_approve"),
	path('admin_leave_staff_reject/<str:leave_id>', adminView.admin_leave_staff_reject, name="admin_leave_staff_reject"),
	path('admin_view_attendance', adminView.admin_view_attendance, name="admin_view_attendance"),
	path('admin_get_attendance_dates', adminView.admin_get_attendance_dates, name="admin_get_attendance_dates"),
	path('admin_get_attendance_students', adminView.admin_get_attendance_students, name="admin_get_attendance_students"),

#staffURL
    path('staff_dashboard', staffView.staff_dashboard, name="staff_dashboard"),
    path('staff_take_attendance', staffView.staff_take_attendance, name="staff_take_attendance"),
    path('staff_get_students', staffView.staff_get_students, name="staff_get_students"),
    path('staff_attendance_data_save', staffView.staff_attendance_data_save, name="staff_attendance_data_save"),
    path('staff_update_attendance_data', staffView.staff_update_attendance_data, name="staff_update_attendance_data"),
    path('staff_update_attendance_data_save', staffView.staff_update_attendance_data_save, name="staff_update_attendance_data_save"),
    path('staff_get_attendance_dates', staffView.staff_get_attendance_dates, name="staff_get_attendance_dates"),
    path('staff_get_attendance_students', staffView.staff_get_attendance_students, name="staff_get_attendance_students"),
    path('staff_apply_leave', staffView.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save', staffView.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback', staffView.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save', staffView.staff_feedback_save, name="staff_feedback_save"),
    path('staff_add_result', staffView.staff_add_result, name="staff_add_result"),
    path('staff_add_result_save', staffView.staff_add_result_save, name="staff_add_result_save"),

#studentURL
    path('student_dashboard', studentView.student_dashboard, name="student_dashboard"),
    path('student_view_attendance', studentView.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post', studentView.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_apply_leave', studentView.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save', studentView.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback', studentView.student_feedback, name="student_feedback"),
    path('student_feedback_save', studentView.student_feedback_save, name="student_feedback_save"),
    path('student_view_result', studentView.student_view_result, name="student_view_result"),
]