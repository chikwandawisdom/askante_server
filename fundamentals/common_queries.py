from django.db.models import Q


def search_by_name(name: str) -> Q:
    """
    This function is used to search by name
    :param name:
    :return:
    """
    if name is None:
        return Q()
    return Q(name__icontains=name)


def search_by_names(first_name: str, last_name: str) -> Q:
    """
    This function is used to search by first name and last name
    :param first_name:
    :param last_name:
    :return:
    """
    if first_name is not None and last_name is None:
        return Q(first_name__icontains=first_name)

    if first_name is None and last_name is not None:
        return Q(last_name__icontains=last_name)

    if first_name is None and last_name is None:
        return Q()

    return Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name)


def search_student_by_name(search):
    if search is None:
        return Q()
    return Q(first_name__icontains=search) | Q(last_name__icontains=search)


def filter_by_institution(institution: int) -> Q:
    """
    This function is used to filter by institution
    :param institution:
    :return:
    """
    if institution is None:
        return Q()
    return Q(institution=institution)
