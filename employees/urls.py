from rest_framework.urls import path

from .views import EmploymentPositionList, EmploymentPositionDetail, EmploymentTypeList, EmploymentTypeDetail, \
    EmployeeList, EmployeeDetail, EmployeeAddressList, EmployeeAddressDetail, EmployeeContactList, EmployeeContactDetail

urlpatterns = [
    path('employment-positions', EmploymentPositionList.as_view(), name='employment_positions'),
    path('employment-positions/<int:pk>', EmploymentPositionDetail.as_view(), name='employment_position'),

    path('employment-types', EmploymentTypeList.as_view(), name='employment_types'),
    path('employment-types/<int:pk>', EmploymentTypeDetail.as_view(), name='employment_type'),

    path('employees', EmployeeList.as_view(), name='employees'),
    path('employees/<int:pk>', EmployeeDetail.as_view(), name='employee'),

    path('employee-addresses', EmployeeAddressList.as_view(), name='employee_addresses'),
    path('employee-addresses/<int:pk>', EmployeeAddressDetail.as_view(), name='employee_address'),

    path('employee-contacts', EmployeeContactList.as_view(), name='employee_contacts'),
    path('employee-contacts/<int:pk>', EmployeeContactDetail.as_view(), name='employee_contact'),
]
