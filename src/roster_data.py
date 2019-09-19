from typing import List

from src.data_model import Departments


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
        lookup_dict[row['Students Username']] = {
            'handshake_id': row['Students ID'],
            'majors': [row['Majors Name']],
            'school_year': row['School Year Name']
        }
        return lookup_dict

    result = {}
    for row in raw_handshake_data:
        if row['Students Username'] not in result:
            result = _add_new_username_to_lookup(row, result)
        else:
            result[row['Students Username']]['majors'].append(row['Majors Name'])
    return result


def transform_major_data(raw_major_data: List[dict]) -> dict:
    """
    Create a lookup dict in the form {major: {department and college info}}

    :param raw_major_data: raw major data as read from a csv
    :return: a dict that allows the lookup of department and college given major
    """
    result = {}
    for row in raw_major_data:
        result[row['major']] = {
            'department': row['department'],
            'college': row['college']
        }
    return result


def enrich_with_handshake_data(student_data: List[dict], handshake_lookup_data: dict) -> List[dict]:
    """
    Enrich student data with Handshake data.

    :param student_data: student data with a 'handshake_username' field
    :param handshake_lookup_data: a Handshake username-to-data lookup dict
    :return: an enriched dataset combining the student data and Handshake data
    """
    result = []
    for row in student_data:
        handshake_record = handshake_lookup_data[row['handshake_username']]
        for major in handshake_record['majors']:
            new_row = row.copy()
            new_row['handshake_id'] = handshake_record['handshake_id']
            new_row['major'] = major
            new_row['school_year'] = handshake_record['school_year']
            result.append(new_row)
    return result


def enrich_with_dept_college_data(student_data: List[dict], dept_college_data: dict) -> List[dict]:
    """
    Enrich student data with appropriate department affiliation and college data.

    :param student_data: student data with 'major' and 'school_year' fields
    :return: an enriched dataset including department affiliations and colleges for each student
    """
    result = []
    for row in student_data:
        new_row = row.copy()
        new_row['department'] = dept_college_data[new_row['major']]['department']
        new_row['college'] = dept_college_data[new_row['major']]['college']
        result.append(new_row)
        if new_row['school_year'] == 'Freshman' and new_row['department'] != 'soar_fye_ksas':
            fye_row = new_row.copy()
            fye_row['department'] = _get_fye_dept_from_college(fye_row['college'])
            result.append(fye_row)
    return result


def _get_fye_dept_from_college(college: str) -> str:
    if college == 'ksas':
        return Departments.SOAR_FYE_KSAS.value.name
    elif college == 'wse':
        return Departments.SOAR_FYE_WSE.value.name
    else:
        raise ValueError(f'Unknown college value "{college}"')
