from typing import List

from src.common import read_csv
from src.student_data_etl.student_data_record import EducationRecord


def extract_major_data(filepath: str) -> dict:
    return transform_major_data(read_csv(filepath))


def extract_handshake_data(filepath: str) -> dict:
    return transform_handshake_data(read_csv(filepath))


def extract_athlete_data(filepath: str) -> dict:
    return transform_athlete_data(read_csv(filepath))


def extract_sis_rosters(roster_filepaths: List[str]) -> List[dict]:
    result = []
    for filepath in roster_filepaths:
        result += transform_roster_data(read_csv(filepath))
    return result


def transform_roster_data(raw_sis_data: List[dict]) -> List[dict]:
    """
    Transform raw SIS student data into a form usable by subsequent data enrichment functions

    :param raw_sis_data: raw data pulled from SIS
    :return: a list of dicts that can be passed to other data enrichment functions
    """
    return [{'handshake_username': row['textbox7']} for row in raw_sis_data]


def transform_handshake_data(raw_handshake_data: List[dict]) -> dict:
    """
    Create a lookup dict in the form {student_username: {info about student}}

    :param raw_handshake_data: raw Handshake student data containing account ID, major and school year info
    :return: a dict that allows the lookup of Handshake data given a username
    """

    def _add_new_username_to_lookup(row: dict, lookup_dict: dict) -> dict:
        lookup_dict[row['Students Username'].upper()] = {
            'handshake_id': row['Students ID'],
            'majors': [row['Majors Name']],
            'school_year': row['School Year Name'],
            'email': row['Students Email'],
            'first_name': row['Students First Name'],
            'pref_name': row['Students Preferred Name'],
            'last_name': row['Students Last Name']
        }
        return lookup_dict

    result = {}
    for row in raw_handshake_data:
        if row['Students Username'].upper() not in result:
            result = _add_new_username_to_lookup(row, result)
        else:
            result[row['Students Username'].upper()]['majors'].append(row['Majors Name'])
    return result


def transform_major_data(raw_major_data: List[dict]) -> dict:
    """
    Create a lookup dict in the form {major: {department and college info}}

    :param raw_major_data: raw major data as read from a csv
    :return: a dict that allows the lookup of department and college given major
    """

    def _convert_empty_str_to_none(value: str):
        if value == '':
            return None
        else:
            return value

    result = {}
    for row in raw_major_data:
        result[row['major']] = EducationRecord(
            major=_convert_empty_str_to_none(row['major']),
            department=_convert_empty_str_to_none(row['department']),
            college=_convert_empty_str_to_none(row['college'])
        )
    return result


def transform_athlete_data(raw_athlete_data: List[dict]) -> dict:
    """
    Create a lookup dict in the form {hopkins_id: sport}

    :param raw_athlete_data: raw athlete data as read from a csv
    :return: a dict that allows the lookup of sports team given hopkins ID
    """
    result = {}
    for row in raw_athlete_data:
        hopkins_id = row['University ID'].upper()
        if hopkins_id not in result:
            result[hopkins_id] = [row['Sport']]
        else:
            result[hopkins_id].append(row['Sport'])
    return result
