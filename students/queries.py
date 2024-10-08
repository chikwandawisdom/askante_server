from django.db.models import Q


def filter_by_student_id(student_id: str) -> Q:
    """
    This function is used to filter by student_id
    :param student_id:
    :return:
    """
    if student_id is None:
        return Q()
    return Q(student_id=student_id)


def filter_by_grade(grade: int) -> Q:
    """
    This function is used to filter by grade
    :param grade:
    :return:
    """
    if grade is None:
        return Q()
    return Q(grade=grade)

def filter_by_gender(gender: int) -> Q:
    """
    This function is used to filter by grade
    :param grade:
    :return:
    """
    if gender is None:
        return Q()
    return Q(gender=gender)


def filter_by_student_type(student_type: int) -> Q:
    """
    This function is used to filter by grade
    :param grade:
    :return:
    """
    if student_type is None:
        return Q()
    return Q(student_type=student_type)


def filter_parents_by_student_id(student_id: str) -> Q:
    """
    This function is used to filter parents by student_id
    :param student_id:
    :return:
    """
    print(student_id)
    if student_id is None:
        return Q()
    return Q(student=student_id)