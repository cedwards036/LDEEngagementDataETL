from collections import defaultdict
from typing import List

from src.common import read_csv, convert_empty_str_to_none
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

    def _append_major_to_lookup_entry(row, result):
        result[row['Students Username'].upper()]['majors'].append(row['Majors Name'])
        return result

    result = {}
    for row in raw_handshake_data:
        if row['Students Username'].upper() not in result:
            result = _add_new_username_to_lookup(row, result)
        else:
            result = _append_major_to_lookup_entry(row, result)
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
