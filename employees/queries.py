from django.db.models import Q

def filter_by_gender(gender: int) -> Q:
    """
    This function is used to filter by grade
    :param grade:
    :return:
    """
    if gender is None:
        return Q()
    return Q(gender=gender)


def search_by_employee_name(search):
    """
    This function is used to search by name
    :param name:
    :return:
    """
    if search is None:
        return Q()
    return Q(first_name__icontains=search) | Q(last_name__icontains=search)
