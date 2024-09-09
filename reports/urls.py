from rest_framework.urls import path

from .views import get_institution_overview, get_last_7_days_attendance, get_last_15_days_finance_data, \
    get_teachers_overview, get_teachers_class_attendance, students_report, teachers_report, attendance_report, \
    get_result_summary, get_result_reports, get_publishers_last_10_days_sales,get_teacher_students,get_teacher_students_list

urlpatterns = [
    path('reports/institution-overview', get_institution_overview, name='get_institution_overview'),
    path('reports/attendance/last-7-days', get_last_7_days_attendance, name='get_last_7_days_attendance'),
    path('reports/finance/last-15-days', get_last_15_days_finance_data, name='get_last_15_days_finance_data'),

    path('reports/teachers-overview', get_teachers_overview, name='get_teachers_overview'),
    path('reports/teachers-students', get_teacher_students, name='get_teacher_students'),
    path('reports/teachers-students-list', get_teacher_students_list, name='get_teacher_students_list'),
    path('reports/teachers-class-attendance', get_teachers_class_attendance, name='get_teachers_class_attendance'),

    path('reports/students-report', students_report, name='students-report'),
    path('reports/teachers-report', teachers_report, name='teachers-report'),
    path('reports/attendance-report', attendance_report, name='attendance-report'),
    path('reports/result-summary', get_result_summary, name='get_result_summary'),
    path('reports/result-reports', get_result_reports, name='get_result_reports'),

    path('reports/publishers-last-10-days-sales', get_publishers_last_10_days_sales, name='get_publishers_last_10_days_sales'),

]
