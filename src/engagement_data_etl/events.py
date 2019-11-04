from typing import List

from autohandshake import HandshakeBrowser

from src.common import InsightsReport, parse_date_string
from src.data_model import EngagementRecord, EngagementTypes, Mediums, Departments, Department
from src.handshake_fields import EventFields

EVENTS_INSIGHTS_REPORT = InsightsReport(
    url='https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZXZlbnRzP3FpZD1XdnpaMTl2N2hJa0d4V0NUTlNQN1U3JmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA==',
    date_field_category='Events',
    date_field_title='Start Date Date'
)

EVENTS_LABELS_INSIGHTS_REPORT = InsightsReport(
    url='https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZXZlbnRzP3FpZD1YeGVFWG9SV0h2NjZSdFBLcTI3NWYwJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA==',
    date_field_category='Events',
    date_field_title='Start Date Date'
)


def run_events_etl(browser: HandshakeBrowser) -> List[EngagementRecord]:
    """
    Run the full ETL process for events data

    :param browser: a logged-in HandshakeBrowser
    :return: a list consisting of cleaned event engagement data
    """
    raw_event_data = EVENTS_INSIGHTS_REPORT.extract_data(browser)
    raw_event_label_data = EVENTS_LABELS_INSIGHTS_REPORT.extract_data(browser)
    return transform_events_data(raw_event_data, raw_event_label_data)


def transform_events_data(raw_events_data: List[dict], raw_events_labels_data: List[dict]) -> List[EngagementRecord]:
    """
    Transform raw events data into standard "engagement data" format

    :param raw_events_data: raw events data from Handshake
    :return: cleaned events data in the form of "engagement data"
    """
    result = []
    dept_data = _build_dept_lookup_dict(raw_events_labels_data)
    for raw_data_row in raw_events_data:
        for department in dept_data[raw_data_row[EventFields.ID]]['depts']:
            result.append(_transform_data_row(raw_data_row, department))
    return result


def _build_dept_lookup_dict(raw_events_labels_data: List[dict]) -> dict:
    dept_data = {}
    for row in raw_events_labels_data:
        dept_data = _ensure_event_is_in_lookup_data(row, dept_data)
        department = _get_department_from_label(row)
        if department is not None:
            dept_data[row[EventFields.ID]] = _add_valid_dept(department, dept_data[row[EventFields.ID]])
        else:
            dept_data[row[EventFields.ID]] = _add_invalid_dept(dept_data[row[EventFields.ID]])
    return dept_data


def _ensure_event_is_in_lookup_data(event_data_row: dict, dept_data: dict) -> dict:
    if event_data_row[EventFields.ID] not in dept_data.keys():
        dept_data[event_data_row[EventFields.ID]] = {'depts': [], 'contains_valid_dept': False}
    return dept_data


def _add_valid_dept(department: Department, dept_record: dict) -> dict:
    if dept_record['contains_valid_dept']:
        dept_record['depts'].append(department)
    else:
        dept_record['depts'] = [department]
        dept_record['contains_valid_dept'] = True
    return dept_record


def _add_invalid_dept(dept_record: dict) -> dict:
    if not dept_record['contains_valid_dept']:
        dept_record['depts'] = [Departments.NO_DEPARTMENT.value]
    return dept_record


def _transform_data_row(raw_data_row: dict, engagement_department: Department) -> EngagementRecord:
    return EngagementRecord(
        engagement_type=EngagementTypes.EVENT,
        handshake_engagement_id=raw_data_row[EventFields.ID],
        start_date_time=parse_date_string(raw_data_row[EventFields.START_DATE_TIME]),
        medium=Mediums.IN_PERSON,
        engagement_name=raw_data_row[EventFields.NAME],
        engagement_department=engagement_department,
        student_handshake_id=raw_data_row[EventFields.STUDENT_ID],
        student_school_year_at_time_of_engagement=None,
        student_pre_registered=_student_pre_registered(raw_data_row),
        associated_staff_email=None
    )


def _student_pre_registered(raw_data_row: dict) -> bool:
    return raw_data_row[EventFields.IS_PRE_REGISTERED] == 'Yes'


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
        return label_to_dept_mapping[raw_data_row[EventFields.LABEL]]
    except KeyError:
        return None
