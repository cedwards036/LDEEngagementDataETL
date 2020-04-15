from collections import defaultdict
from datetime import datetime, timedelta
from typing import List

from src.common import InsightsReport, HandshakeBrowser
from src.common import read_csv, convert_empty_str_to_none
from src.handshake_fields import StudentFields
from src.student_data_etl.student_data_record import EducationRecord

STUDENTS_INSIGHTS_REPORT = InsightsReport(
    url='https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPVVBWjNRTzZIcTB5cUprSEtFbFQ4cG0mZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9Zmls',
)

def extract_major_data(filepath: str) -> dict:
    return transform_major_data(read_csv(filepath))


def extract_handshake_data(browser: HandshakeBrowser) -> List[dict]:
    return transform_handshake_data(
        filter_handshake_data(datetime.today(), STUDENTS_INSIGHTS_REPORT.extract_data(browser))
    )


def extract_athlete_data(filepath: str) -> dict:
    return transform_athlete_data(read_csv(filepath))


def filter_handshake_data(current_date: datetime, handshake_data: List[dict]) -> List[dict]:
    def has_good_date_label(data_row: dict) -> bool:
        good_labels = [f"temp: {(current_date - timedelta(days=i)).strftime('%Y-%m-%d')}" for i in range(4)]
        for label in good_labels:
            if label in data_row[StudentFields.LABELS]:
                return True
        return False

    def is_not_ep(data_row: dict) -> bool:
        return 'system gen: ep' not in data_row[StudentFields.LABELS]

    def does_not_have_hwd_location_label(data_row: dict) -> bool:
        return 'system gen: hwd location' not in data_row[StudentFields.LABELS]

    def is_homewood_undergrad_or_masters(data_row):
        return has_good_date_label(data_row) and is_not_ep(data_row) and \
               does_not_have_hwd_location_label(data_row)

    return list(filter(is_homewood_undergrad_or_masters, handshake_data))


def transform_handshake_data(raw_handshake_data: List[dict]) -> List[dict]:
    def _determine_first_name(row: dict) -> str:
        if row[StudentFields.PREF_NAME]:
            return row[StudentFields.PREF_NAME]
        else:
            return row[StudentFields.FIRST_NAME]

    def _transform_row(row: dict) -> dict:
        return {
            'handshake_username': row[StudentFields.USERNAME],
            'handshake_id': row[StudentFields.ID],
            'majors': [row[StudentFields.MAJOR]],
            'school_year': row[StudentFields.SCHOOL_YEAR],
            'email': row[StudentFields.EMAIL],
            'first_name': _determine_first_name(row),
            'legal_first_name': row[StudentFields.FIRST_NAME],
            'pref_first_name': row[StudentFields.PREF_NAME],
            'last_name': row[StudentFields.LAST_NAME],
            'has_activated_handshake': row[StudentFields.HAS_LOGGED_IN] == 'Yes',
            'has_completed_profile': row[StudentFields.HAS_COMPLETED_PROFILE] == 'Yes',
            'is_pre_med': 'hwd: pre-health' in row[StudentFields.LABELS]
        }

    result = []
    lookup = {}
    for row in raw_handshake_data:
        if row[StudentFields.USERNAME] not in lookup:
            transformed_row = _transform_row(row)
            lookup[row[StudentFields.USERNAME]] = transformed_row
            result.append(transformed_row)
        else:
            lookup[row[StudentFields.USERNAME]]['majors'].append(row[StudentFields.MAJOR])
    return result


def transform_major_data(raw_major_data: List[dict]) -> dict:
    """
    Create a lookup dict in the form {major: {department and college info}}

    :param raw_major_data: raw major data as read from a csv
    :return: a dict that allows the lookup of department and college given major
    """
    return {
        row['major']: EducationRecord(
            major=convert_empty_str_to_none(row['major']),
            department=convert_empty_str_to_none(row['department']),
            college=convert_empty_str_to_none(row['college']))
        for row in raw_major_data
    }


def transform_athlete_data(raw_athlete_data: List[dict]) -> dict:
    """
    Create a lookup dict in the form {hopkins_id: sport}

    :param raw_athlete_data: raw athlete data as read from a csv
    :return: a dict that allows the lookup of sports team given hopkins ID
    """
    result = defaultdict(list)
    for row in raw_athlete_data:
        result[row['University ID'].upper()].append(row['Sport'])
    return result
