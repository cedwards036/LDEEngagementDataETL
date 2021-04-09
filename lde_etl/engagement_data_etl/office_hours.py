from typing import List

from autohandshake import HandshakeBrowser

from lde_etl.common import InsightsReport, parse_date_string, RangeInsightsDateField
from lde_etl.data_model import Departments, Department, EngagementRecord, EngagementTypes, Mediums
from lde_etl.handshake_fields import AppointmentFields

APPT_INSIGHTS_REPORT = InsightsReport(
    url='https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vYXBwb2ludG1lbnRzP3FpZD1FN3dFaTlXWkpWWktKeElVT0FZbE1lJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA==',
    date_field=RangeInsightsDateField(date_field_category='Appointments',
                                      date_field_title='Start Date Date')
)


def run_office_hours_etl(browser: HandshakeBrowser, download_dir) -> List[EngagementRecord]:
    """
    Run the full ETL process for Office Hours data

    :param browser: a logged-in HandshakeBrowser
    :return: a list consisting of cleaned office hour engagement data
    """
    raw_appt_data = APPT_INSIGHTS_REPORT.extract_data(browser, download_dir)
    return transform_office_hours_data(raw_appt_data)


def transform_office_hours_data(raw_data: List[dict]) -> List[EngagementRecord]:
    """
    Transform raw office hours data into standard "engagement data" format

    :param raw_data: raw office hours data from Handshake
    :return: cleaned office hours data in the form of "engagement data"
    """
    return list(map(_transform_data_row, raw_data))


def _transform_data_row(raw_data_row: dict) -> EngagementRecord:
    department = _get_department_from_type(raw_data_row)
    return EngagementRecord(
        engagement_type=EngagementTypes.OFFICE_HOURS,
        handshake_engagement_id=raw_data_row[AppointmentFields.ID],
        start_date_time=parse_date_string(raw_data_row[AppointmentFields.START_DATE_TIME]),
        medium=_get_medium(raw_data_row),
        engagement_name=_make_engagement_name(raw_data_row, department),
        engagement_department=department,
        student_handshake_id=raw_data_row[AppointmentFields.STUDENT_ID],
        student_school_year_at_time_of_engagement=raw_data_row[AppointmentFields.STUDENT_SCHOOL_YEAR],
        student_pre_registered=_student_pre_registered(raw_data_row),
        associated_staff_email=raw_data_row[AppointmentFields.STAFF_MEMBER_EMAIL]
    )


def _make_engagement_name(raw_data_row: dict, department: Department) -> str:
    if department == Departments.PRE_PROF.value:
        return f'{raw_data_row[AppointmentFields.TYPE]} Appointment'
    else:
        return f'{raw_data_row[AppointmentFields.TYPE]} Office Hours'


def _get_medium(raw_data_row: dict) -> Mediums:
    lower_medium_str = raw_data_row[AppointmentFields.MEDIUM].lower()
    if 'in-person' in lower_medium_str:
        return Mediums.IN_PERSON
    elif 'virtual' in lower_medium_str or 'phone' in lower_medium_str:
        return Mediums.VIRTUAL
    elif 'email' in lower_medium_str:
        return Mediums.EMAIL
    else:
        raise ValueError(f'Unknown medium: {raw_data_row[AppointmentFields.MEDIUM]}')


def _get_department_from_type(raw_data_row: dict) -> Department:
    appt_type_to_dept_mapping = {
        'Homewood: AMS Career Advising - For FM, AMS, and Data Science Graduate Students': Departments.AMS_FM_DATA_SCI,
        '(Archived) Homewood: Biological and Brain Sciences': Departments.BIO_BRAIN_SCI,
        'Homewood: AMS Undergraduates': Departments.AMS_UGRAD,
        '(Archived) Homewood: Biological Sciences': Departments.BIO_SCI,
        'Homewood: Brain Sciences': Departments.BRAIN_SCI,
        'Homewood: Biomedical Engineering': Departments.BME,
        '(Archived) Homewood: ChemBE and Materials Science Engineering': Departments.CHEMBE_MAT_SCI,
        'Homewood: ChemBE': Departments.CHEMBE,
        'Homewood: Civil Engineering': Departments.CIVIL_ENG,
        'Homewood: Computer Science, Computer Engineering, and Electrical Engineering': Departments.COMP_ELEC_ENG,
        'Homewood: Engineering Masters Students': Departments.ENG_MASTERS,
        'Homewood: Environmental Engineering': Departments.ENV_ENG,
        '(Archived) Homewood: Humanities: History, Philosophy, and Humanistic Thought': Departments.HIST_PHIL_HUM,
        '(Archived) Homewood: Humanities: Language, Literatures, Film and Media': Departments.LIT_LANG_FILM,
        '(Archived) Homewood: History': Departments.HISTORY,
        'Homewood: Humanities': Departments.HUMANITIES,
        'Homewood: Materials Science Engineering': Departments.MAT_SCI,
        'Homewood: Mechanical Engineering': Departments.MECH_ENG,
        '(Archived) Homewood: Misc. Engineering': Departments.MISC_ENG,
        'Homewood: Peer Advisor Drop In': Departments.PA_DROP_INS,
        '(Archived) Homewood: Physical and Environmental Sciences': Departments.PHYS_ENV_SCI,
        'Homewood: Pre-Health and Public Health Studies': Departments.PRE_PUB_HEALTH,
        'Homewood: Sciences': Departments.SCIENCES,
        'Homewood: SOAR: Athletics': Departments.SOAR_ATHLETICS,
        'Homewood: SOAR: CSS': Departments.SOAR_CSS,
        'Homewood: SOAR: Diversity and Inclusion': Departments.SOAR_DIV_INCL,
        'Homewood: SOAR: First Year Experience (KSAS)': Departments.SOAR_FYE_KSAS,
        'Homewood: SOAR: First Year Experience (WSE)': Departments.SOAR_FYE_WSE,
        'Homewood: SOAR: Student Leadership and Involvement': Departments.SOAR_SLI,
        'Homewood: Social Sciences': Departments.SOCIAL_SCI,
        '(Archived) Homewood: Social Sciences: International Studies, Sociology, and Anthropology': Departments.INT_SOC_ANTH,
        '(Archived) Homewood: Social Sciences: Political Science, Economics, and Finance': Departments.POL_ECON_FIN,
        'Homewood: Arts, Media, and Marketing Academy': Departments.AMM_ACADEMY,
        'Homewood: Nonprofit and Government Academy': Departments.NP_GOV_ACADEMY,
        'Homewood: Consulting Academy': Departments.CONSUTING_ACADEMY,
        'Homewood: Finance Academy': Departments.FINANCE_ACADEMY,
        'Homewood: Health Sciences Academy': Departments.HEALTH_SCI_ACADEMY,
        'Homewood: STEM and Innovation Academy': Departments.STEM_ACADEMY,
        'Homewood: Pre-Law': Departments.PRE_PROF,
        'Homewood: Pre-Health/Other Health Professions': Departments.PRE_PROF,
        '(Archived) Homewood: Pre-Health/Other Health Professions': Departments.PRE_PROF,
        'Homewood: Pre-Health': Departments.PRE_PROF,
        '(Archived) Homewood: Pre-Health (All Education Levels)': Departments.PRE_PROF,
        'Homewood: Pre-Health (Freshmen)': Departments.PRE_PROF,
        '(Archived) Homewood: Pre-Dental': Departments.PRE_PROF,
        'Homewood: Pre-Med': Departments.PRE_PROF,
        '(Archived) Homewood: Pre-Med': Departments.PRE_PROF,
        'Homewood: Non-Office Hour Interaction': Departments.NO_DEPARTMENT,
        'Homewood: Underclassmen Pre-Health': Departments.PRE_PROF,
        'Homewood: Operations': Departments.OPERATIONS
    }
    return appt_type_to_dept_mapping[raw_data_row[AppointmentFields.TYPE]].value


def _student_pre_registered(raw_data_row: dict) -> bool:
    return raw_data_row[AppointmentFields.IS_DROP_IN] == 'No'
