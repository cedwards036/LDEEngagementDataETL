from typing import List

from src.common import InsightsReport, parse_date_string
from src.data_model import EngagementRecord, EngagementTypes, Mediums, Departments, Department

EVENTS_INSIGHTS_REPORT = InsightsReport(
    url='https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZXZlbnRzP3FpZD1YeGVFWG9SV0h2NjZSdFBLcTI3NWYwJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA==',
    date_field_category='Events',
    date_field_title='Start Date Date'
)


def transform_events_data(raw_data: List[dict]) -> List[EngagementRecord]:
    """
    Transform raw events data into standard "engagement data" format

    :param raw_data: raw events data from Handshake
    :return: cleaned events data in the form of "engagement data"
    """
    result = []
    for raw_data_row in raw_data:
        if raw_data_row['added_institution_labels_on_events.name'] is not None:
            department = _get_department_from_label(raw_data_row)
        else:
            department = Departments.NO_DEPARTMENT.value
        if department is not None:
            result.append(_transform_data_row(raw_data_row, department))
    return result


def _transform_data_row(raw_data_row: dict, engagement_department: Department) -> EngagementRecord:
    return EngagementRecord(
        engagement_type=EngagementTypes.EVENT,
        handshake_engagement_id=raw_data_row['events.id'],
        start_date_time=parse_date_string(raw_data_row['events.start_date_time']),
        medium=Mediums.IN_PERSON,
        engagement_name=raw_data_row['events.name'],
        engagement_department=engagement_department,
        student_handshake_id=raw_data_row['attendee_users_on_events.id'],
        student_school_year_at_time_of_engagement=None,
        student_pre_registered=_student_pre_registered(raw_data_row),
        associated_staff_email=None
    )


def _student_pre_registered(raw_data_row: dict) -> bool:
    return raw_data_row['attendees_on_events.registered'] == 'Yes'


def _get_department_from_label(raw_data_row: dict):
    label_to_dept_mapping = {
        'hwd: fm and ams graduate students': Departments.AMS_FM_DATA_SCI.value,
        'hwd: bio and brain sci dept': Departments.BIO_BRAIN_SCI.value,
        'hwd: bme dept': Departments.BME.value,
        'hwd: chembe and mat sci dept': Departments.CHEMBE_MAT_SCI.value,
        'hwd: comp sci and electrical eng dept': Departments.COMP_ELEC_ENG.value,
        'hwd: eng masters students': Departments.ENG_MASTERS.value,
        'hwd: history, phil, and hum dept': Departments.HIST_PHIL_HUM.value,
        'hwd: lang, lit, film and media dept': Departments.LIT_LANG_FILM.value,
        'hwd: poli sci, econ, and finance dept': Departments.POL_ECON_FIN.value,
        'hwd: misc eng dept': Departments.MISC_ENG.value,
        'hwd: physical and env sci dept': Departments.PHYS_ENV_SCI.value,
        'hwd: pre-health and pub health dept': Departments.PRE_PUB_HEALTH.value,
        'hwd: soar athletics': Departments.SOAR_ATHLETICS.value,
        'hwd: soar fye ksas': Departments.SOAR_FYE_KSAS.value,
        'hwd: soar fye wse': Departments.SOAR_FYE_WSE.value,
        'hwd: soar sli': Departments.SOAR_SLI.value,
        'hwd: intl studies, soc, and anth dept': Departments.INT_SOC_ANTH.value,
        'hwd: arts, media, and marketing academy': Departments.AMM_ACADEMY.value,
        'hwd: nonprofit & government academy': Departments.NP_GOV_ACADEMY.value,
        'hwd: consulting academy': Departments.CONSUTING_ACADEMY.value,
        'hwd: finance academy': Departments.FINANCE_ACADEMY.value,
        'hwd: health sciences academy': Departments.HEALTH_SCI_ACADEMY.value,
        'hwd: stem & innovation academy': Departments.STEM_ACADEMY.value,
    }
    try:
        return label_to_dept_mapping[raw_data_row['added_institution_labels_on_events.name']]
    except KeyError:
        return None
