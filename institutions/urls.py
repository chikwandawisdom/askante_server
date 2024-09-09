from rest_framework.urls import path

from .views import create_institution, get_institutions, GradeList, GradeView, SubjectList, SubjectDetail, ClassList, \
    ClassDetails, ClassSubjectList, ClassSubjectDetails, add_students_to_class, get_students_in_class, \
    remove_student_from_class, AcademicYearList, AcademicYearDetails, TermsList, TermsDetails, RoomList, RoomDetails, \
    add_period, get_periods_of_a_class, update_period, delete_period, LevelList, LevelDetails, change_academic_year, \
    get_organizations, create_organization, update_organization, get_invoices, edit_institution

urlpatterns = [

    path('organizations', get_organizations, name='get_organizations'),
    path('organizations/create', create_organization, name='create_organization'),
    path('organizations/update/<int:pk>', update_organization, name='update_organization'),

    path('institutions/create', create_institution, name='create_institution'),
    path('institutions', get_institutions, name='get_institutions'),
    path('institutions/edit/<int:pk>', edit_institution, name='edit_institution'),

    path('levels', LevelList.as_view(), name='levels'),
    path('levels/<int:pk>', LevelDetails.as_view(), name='level'),

    path('grades', GradeList.as_view(), name='grades'),
    path('grades/<int:pk>', GradeView.as_view(), name='grade'),

    path('subjects', SubjectList.as_view(), name='subjects'),
    path('subjects/<int:pk>', SubjectDetail.as_view(), name='subject'),

    path('classes', ClassList.as_view(), name='classes'),
    path('classes/<int:pk>', ClassDetails.as_view(), name='class'),

    path('classes/subjects', ClassSubjectList.as_view(), name='class-subjects'),
    path('classes/subjects/<int:pk>', ClassSubjectDetails.as_view(), name='class-subject'),

    path('classes/add-students', add_students_to_class, name='add-students-to-class'),
    path('classes/students', get_students_in_class, name='get-students-in-class'),
    path('classes/remove-student', remove_student_from_class, name='remove-student-from-class'),

    path('academic-years', AcademicYearList.as_view(), name='academic-years'),
    path('academic-years/<int:pk>', AcademicYearDetails.as_view(), name='academic-year'),

    path('terms', TermsList.as_view(), name='terms'),
    path('terms/<int:pk>', TermsDetails.as_view(), name='term'),

    path('rooms', RoomList.as_view(), name='rooms'),
    path('rooms/<int:pk>', RoomDetails.as_view(), name='room'),

    path('add-period', add_period, name='add-period'),
    path('update-period/<int:pk>', update_period, name='update-period'),
    path('get-periods', get_periods_of_a_class, name='get-periods'),
    path('delete-period/<int:pk>', delete_period, name='delete-period'),

    path('institution/change-academic-year', change_academic_year, name='change-academic-year'),

    path('invoices', get_invoices, name='get_invoices'),
]
