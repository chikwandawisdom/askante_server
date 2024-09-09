from rest_framework.urls import path

from .views import StudentList, StudentDetail, ParentListView, ParentDetailView, StudentContactList, \
    StudentContactDetail, StudentAddressList, StudentAddressDetail, StudentTypeList, StudentTypeDetail

urlpatterns = [
    path('students', StudentList.as_view(), name='students_list'),
    path('students/<int:pk>', StudentDetail.as_view(), name='students_detail'),

    path('parents', ParentListView.as_view(), name='parents_list'),
    path('parents/<int:pk>', ParentDetailView.as_view(), name='parents_detail'),

    path('student-contacts', StudentContactList.as_view(), name='student_contacts_list'),
    path('student-contacts/<int:pk>', StudentContactDetail.as_view(), name='student_contacts_detail'),

    path('student-addresses', StudentAddressList.as_view(), name='student_addresses_list'),
    path('student-addresses/<int:pk>', StudentAddressDetail.as_view(), name='student_addresses_detail'),

    path('student-types', StudentTypeList.as_view(), name='student_types_list'),
    path('student-types/<int:pk>', StudentTypeDetail.as_view(), name='student_types_detail'),
]
