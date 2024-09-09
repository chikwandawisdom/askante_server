from institutions.models.academic_years import AcademicYear
from institutions.models.institution import Institution


def get_active_academic_year(institution: Institution):
    """
    This method returns the current academic year.
    """
    active_academic_year = AcademicYear.objects.filter(institution=institution, is_active=True).first()
    return active_academic_year
