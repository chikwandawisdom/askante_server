from django.db.models import Q


def filter_by_class_subject(class_subject):
    """
    Filter periods by class subject
    :param class_subject: pk
    :return: Q()
    """
    if class_subject is not None:
        return Q(class_subject=class_subject)
    return Q()


def filter_by_period_day(day):
    """
    Filter periods by day
    :param day: day
    :return: Q()
    """
    if day is not None:
        return Q(day=day)
    return Q()


def filter_by_academic_year(academic_year):
    """
    Filter periods by academic year
    :param academic_year: pk
    :return: Q()
    """
    if academic_year is not None:
        return Q(academic_year=academic_year)
    return Q()