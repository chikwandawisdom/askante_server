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


def filter_by_grade(grade: int) -> Q:
    """
    This function is used to filter by grade
    :param grade:
    :return:
    """
    if grade is None:
        return Q()
    return Q(grade=grade)


def filter_by_subject(subject):
    """
    Filter periods by class subject
    :param class_subject: pk
    :return: Q()
    """
    if subject is not None:
        return Q(subject=subject)
    return Q()


def filter_by_type(type):
    """
    Filter periods by class type
    :param class_subject: pk
    :return: Q()
    """
    if type is not None:
        return Q(type=type)
    return Q()


def filter_by_syllabus(syllabus):
    """
    Filter periods by class syllabus
    :param class_subject: pk
    :return: Q()
    """
    if syllabus is not None:
        return Q(syllabus=syllabus)
    return Q()


def filter_by_level(level):
    """
    Filter periods by class level
    :param class_subject: pk
    :return: Q()
    """
    if level is not None:
        return Q(level=level)
    return Q()