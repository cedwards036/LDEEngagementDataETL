from datetime import datetime
from typing import List

from autohandshake import HandshakeBrowser, InsightsPage, FileType

from src.data_model import Departments, Department, EngagementRecord, EngagementTypes, Mediums
from src.utils import CONFIG, read_and_delete_json


def extract_office_hours_data(browser: HandshakeBrowser) -> List[dict]:
    """
    Extract all Handshake office-hours data for the report.

    :param browser: a logged-in HandshakeBrowser
    :return: the raw, extracted data in list-of-dict format
    """
    APPTS_INSIGHTS_URL = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vYXBwb2ludG1lbnRzP3FpZD02QlpEZlFQbTFLcGR3dzN5Rzl2eEFNJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='
    insights_page = InsightsPage(APPTS_INSIGHTS_URL, browser)
    insights_page = _set_report_date_range(insights_page)
    downloaded_filepath = insights_page.download_file(CONFIG['download_dir'], file_type=FileType.JSON)
    return read_and_delete_json(downloaded_filepath)


def transform_office_hours_data(raw_data: List[dict]) -> List[EngagementRecord]:
    """
    Transform raw office hours data into standard "engagement data" format

    :param raw_data: raw office hours data from Handshake
    :return: cleaned office hours data in the form of "engagement data"
    """
    return list(map(_transform_data_row, raw_data))


def _transform_data_row(raw_data_row: dict) -> EngagementRecord:
    return EngagementRecord(
        engagement_type=EngagementTypes.OFFICE_HOURS,
        engagement_id=raw_data_row['appointments.id'],
        start_date_time=_get_start_date_time(raw_data_row),
        medium=_get_medium(raw_data_row),
        engagement_name=raw_data_row['appointment_type_on_appointments.name'],
        engagement_department=_get_department_from_type(raw_data_row),
        student_handshake_id=raw_data_row['student_on_appointments.id'],
        student_school_year_at_time_of_engagement=raw_data_row['student_school_year_on_appointments.name'],
        student_pre_registered=_student_pre_registered(raw_data_row),
        associated_staff_email=raw_data_row['staff_member_on_appointments.email_address']
    )
    # return {
    #     'engagement_type': 'office_hours',
    #     'engagement_id': raw_data_row['appointments.id'],
    #     'start_date_time': _get_start_date_time(raw_data_row),
    #     'medium': _get_medium(raw_data_row),
    #     'engagement_name': raw_data_row['appointment_type_on_appointments.name'],
    #     'engagement_category': department.category,
    #     'engagement_department': department.name,
    #     'student_handshake_id': raw_data_row['student_on_appointments.id'],
    #     'student_school_year_at_time_of_engagement': raw_data_row['student_school_year_on_appointments.name'],
    #     'student_pre_registered': _student_pre_registered(raw_data_row),
    #     'associated_staff_email': raw_data_row['staff_member_on_appointments.email_address']
    # }


def _set_report_date_range(insights_page: InsightsPage):
    START_DATE = datetime(2019, 7, 1)
    END_DATE = datetime.today()
    insights_page.set_date_range_filter(field_category='Appointments', field_title='Start Date Date',
                                        start_date=START_DATE, end_date=END_DATE)
    return insights_page


def _get_medium(raw_data_row: dict) -> Mediums:
    lower_medium_str = raw_data_row['appointment_medium_on_appointments.name'].lower()
    if 'in-person' in lower_medium_str:
        return Mediums.IN_PERSON
    elif 'virtual' in lower_medium_str:
        return Mediums.VIRTUAL
    else:
        raise ValueError(f'Unknown medium: {raw_data_row["appointment_medium_on_appointments.name"]}')


def _get_start_date_time(raw_data_row: dict) -> datetime:
    return datetime.strptime(raw_data_row['appointments.start_date_time'], '%Y-%m-%d %H:%M:%S')


def _get_department_from_type(raw_data_row: dict) -> Department:
    appt_type_to_dept_mapping = {
        'Homewood: AMS Career Advising - For FM, AMS, and Data Science Graduate Students': Departments.AMS_FM_DATA_SCI.value,
        'Homewood: Biological and Brain Sciences': Departments.BIO_BRAIN_SCI.value,
        'Homewood: Biomedical Engineering': Departments.BME.value,
        'Homewood: ChemBE and Materials Science Engineering': Departments.CHEMBE_MAT_SCI.value,
        'Homewood: Computer Science, Computer Engineering, and Electrical Engineering': Departments.COMP_ELEC_ENG.value,
        'Homewood: Engineering Masters Students': Departments.ENG_MASTERS.value,
        'Homewood: Humanities: History, Philosophy,and Humanistic Thought': Departments.HIST_PHIL_HUM.value,
        'Homewood: Humanities: Language, Literatures, Film and Media': Departments.LIT_LANG_FILM.value,
        'Homewood: Social Sciences: Political Science, Economics, and Finance': Departments.POL_ECON_FIN.value,
        'Homewood: Misc Engineering': Departments.MISC_ENG.value,
        'Homewood: Peer Advisor Drop In': Departments.PA_DROP_INS.value,
        'Homewood: Physical and Environmental Sciences': Departments.PHYS_ENV_SCI.value,
        'Homewood: Pre-Health and Public Health Studies': Departments.PRE_PUB_HEALTH.value,
        'Homewood: SOAR: Athletics': Departments.SOAR_ATHLETICS.value,
        'Homewood: SOAR: First Year Experience (KSAS)': Departments.SOAR_FYE_KSAS.value,
        'Homewood: SOAR: First Year Experience (WSE)': Departments.SOAR_FYE_WSE.value,
        'Homewood: SOAR: Student Leadership and Involvement': Departments.SOAR_SLI.value,
        'Homewood: Social Sciences: International Studies, Sociology, and Anthropology': Departments.INT_SOC_ANTH.value,
        'Homewood: Arts, Media, and Marketing Academy': Departments.AMM_ACADEMY.value,
        'Homewood: Nonprofit and Government Academy': Departments.NP_GOV_ACADEMY.value,
        'Homewood: Consulting Academy': Departments.CONSUTING_ACADEMY.value,
        'Homewood: Finance Academy': Departments.FINANCE_ACADEMY.value,
        'Homewood: Health Sciences Academy': Departments.HEALTH_SCI_ACADEMY.value,
        'Homewood: STEM and Innovation Academy': Departments.STEM_ACADEMY.value,
        'Homewood: Pre-Law': Departments.PRE_PROF.value,
        'Homewood: Pre-Health/Other Health Professions': Departments.PRE_PROF.value,
        'Homewood: Pre-Dental': Departments.PRE_PROF.value,
        'Homewood: Pre-Med': Departments.PRE_PROF.value
    }
    return appt_type_to_dept_mapping[raw_data_row['appointment_type_on_appointments.name']]


def _student_pre_registered(raw_data_row: dict) -> bool:
    return raw_data_row['appointments.walkin'] == 'No'
