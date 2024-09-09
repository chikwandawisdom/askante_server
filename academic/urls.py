from rest_framework.urls import path

from .views import get_teachers_class_list, get_teachers_periods, submit_attendance, get_attendance_list, \
    MarkingCriterionList, MarkingCriterionDetail, AssignmentList, AssignmentDetail, ExamList, ExamDetail, \
    get_teachers_monthly_calendar, get_marking_options_for_a_class, MarkList, MarkDetail, get_students_monthly_calendar, \
    get_attendance_list_for_student, get_assignments_for_student, get_exams_for_students, \
    get_class_subject_list_for_students, get_periods_for_students, submit_term_result, get_term_result, get_settings, \
    update_settings, get_student_marks, get_student_term_results

urlpatterns = [
    path('teachers/class-list', get_teachers_class_list, name='get_teachers_class_list'),
    path('teachers/periods', get_teachers_periods, name='get_teachers_periods'),
    path('teachers/submit-attendance', submit_attendance, name='submit_attendance'),
    path('teachers/attendance-list', get_attendance_list, name='get_attendance_list'),

    path('marking-criterion', MarkingCriterionList.as_view(), name='marking_criterion_list'),
    path('marking-criterion/<int:pk>', MarkingCriterionDetail.as_view(), name='marking_criterion_detail'),

    path('teachers/assignments', AssignmentList.as_view(), name='assignment_list'),
    path('teachers/assignments/<int:pk>', AssignmentDetail.as_view(), name='assignment_detail'),

    path('teachers/exams', ExamList.as_view(), name='exam_list'),
    path('teachers/exams/<int:pk>', ExamDetail.as_view(), name='exam_detail'),

    path('teachers/monthly-calendar', get_teachers_monthly_calendar, name='get_teachers_monthly_calendar'),

    path('teachers/marking-options', get_marking_options_for_a_class, name='get_marking_options_for_a_class'),

    path('teachers/submit-term-result', submit_term_result, name='submit_term_result'),
    path('teachers/term-result', get_term_result, name='get_term_result'),

    path('teachers/marks', MarkList.as_view(), name='mark_list'),
    path('teachers/marks/<int:pk>', MarkDetail.as_view(), name='mark_detail'),

    path('students/monthly-calendar', get_students_monthly_calendar, name='get_students_monthly_calendar'),
    path('students/attendance-list', get_attendance_list_for_student, name='get_attendance_list_for_student'),
    path('students/assignments', get_assignments_for_student, name='get_assignments_for_student'),
    path('students/exams', get_exams_for_students, name='get_exams_for_students'),
    path('students/class-subject-list', get_class_subject_list_for_students,
         name='get_class_subject_list_for_students'),
    path('students/periods', get_periods_for_students, name='get_periods_for_students'),
    path('students/marks', get_student_marks, name='get_student_marks'),
    path('students/term-results', get_student_term_results, name='get_student_term_results'),

    path("academic/settings", get_settings, name="get_academic_settings"),
    path("academic/settings/update", update_settings, name="update_academic_settings"),
]
