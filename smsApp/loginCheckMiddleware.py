from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class loginCheckMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user

        if user.is_authenticated:
            if user.user_type == '1':
                if modulename == 'smsApp.adminView':
                    pass
                elif modulename == 'smsApp.views' or modulename == 'django.views.static':
                    pass
                else:
                    return HttpResponseRedirect(reverse('admin_dashboard'))

            elif user.user_type == '2':
                if modulename == 'smsApp.staffView':
                    pass
                elif modulename == 'smsApp.views' or modulename == 'django.views.static':
                    pass
                else:
                    return HttpResponseRedirect(reverse('staff_dashboard'))

            elif user.user_type == '3':
                if modulename == 'smsApp.studentView':
                    pass
                elif modulename == 'smsApp.views' or modulename == 'django.views.static':
                    pass
                else:
                    return HttpResponseRedirect(reverse('student_dashboard'))

            else:
                return HttpResponseRedirect(reverse('showLogin'))
        else:
            if request.path == reverse('showLogin') or request.path == reverse('userLogin'):
                pass
            else:
                return HttpResponseRedirect(reverse('showLogin'))