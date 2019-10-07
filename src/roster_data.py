from typing import List

from src.common import read_csv
from src.data_model import Departments


def run_students_etl(sis_roster_filepaths: List[str], handshake_data_filepath: str,
                     major_data_filepath: str, athlete_filepath: str) -> List[dict]:
    major_data = _extract_major_data(major_data_filepath)
    handshake_data = _extract_handshake_data(handshake_data_filepath)
    roster_data = _extract_sis_rosters(sis_roster_filepaths)
    athlete_data = _extract_athlete_data(athlete_filepath)
    return enrich_with_athlete_data(
        enrich_with_dept_college_data(
            enrich_with_handshake_data(roster_data, handshake_data),
            major_data),
        athlete_data)


def _extract_major_data(filepath: str) -> dict:
    return transform_major_data(read_csv(filepath))


def _extract_handshake_data(filepath: str) -> dict:
    return transform_handshake_data(read_csv(filepath))


def _extract_athlete_data(filepath: str) -> dict:
    return transform_athlete_data(read_csv(filepath))


def _extract_sis_rosters(roster_filepaths: List[str]) -> List[dict]:
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
            'school_year': row['School Year Name']
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
    result = {}
    for row in raw_major_data:
        result[row['major']] = {
            'department': row['department'],
            'college': row['college']
        }
    return result


def transform_athlete_data(raw_athlete_data: List[dict]) -> dict:
    """
    Create a lookup dict in the form {hopkins_id: sport}

    :param raw_athlete_data: raw athlete data as read from a csv
    :return: a dict that allows the lookup of sports team given hopkins ID
    """
    result = {}
    for row in raw_athlete_data:
        result[row['University ID'].upper()] = row['Sport']
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
        handshake_record = handshake_lookup_data[row['handshake_username'].upper()]
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
    :param dept_college_data: a dict mapping username to dept and college data
    :return: an enriched dataset including department affiliations and colleges for each student
    """

    def _clean_major(major: str) -> str:
        colon_loc = major.find(':')
        if colon_loc == -1 or _is_masters_degree(major):
            return major
        else:
            return major[colon_loc + 1:].strip()

    def _is_masters_degree(major: str) -> bool:
        masters_prefixes = ['M.S.E.', 'M.A.', 'M.S.', 'M.F.A']
        for prefix in masters_prefixes:
            if major.startswith(prefix):
                return True
        return False


    def _enrich_row(row: dict) -> dict:
        new_row = row.copy()
        new_row['department'] = dept_college_data[new_row['major']]['department']
        new_row['college'] = dept_college_data[new_row['major']]['college']
        new_row['major'] = _clean_major(new_row['major'])
        return new_row

    def _student_is_freshman_with_defined_major(row: dict) -> bool:
        return row['school_year'] == 'Freshman' and row['department'] != 'soar_fye_ksas'

    def _enrich_fye_row(row: dict) -> dict:
        fye_row = row.copy()
        fye_row['department'] = _get_fye_dept_from_college(fye_row['college'])
        new_row['major'] = _clean_major(new_row['major'])
        return fye_row

    def _get_fye_dept_from_college(college: str) -> str:
        if college == 'ksas':
            return Departments.SOAR_FYE_KSAS.value.name
        elif college == 'wse':
            return Departments.SOAR_FYE_WSE.value.name
        else:
            raise ValueError(f'Unknown college value "{college}"')

    def _enrich_no_dept_row(row: dict) -> dict:
        new_row = row.copy()
        new_row['department'] = None
        new_row['college'] = None
        new_row['major'] = _clean_major(new_row['major'])
        return new_row

    result = []
    for row in student_data:
        try:
            new_row = _enrich_row(row)
            result.append(new_row)
            if _student_is_freshman_with_defined_major(new_row):
                result.append(_enrich_fye_row(new_row))
        except KeyError:  # when there is no lookup match for the student's major
            if row['major'] == '' or ('interdisciplinary studies' in row['major'].lower()):
                result.append(_enrich_no_dept_row(row))
            else:
                raise ValueError(f'Student {row["handshake_username"]} has unexpected major "{row["major"]}"')
    return result


def enrich_with_athlete_data(student_data: List[dict], athlete_data: dict) -> List[dict]:
    """
    Enrich student data with appropriate department affiliation and college data.

    :param student_data: student data with a 'handshake_username' field
    :param athlete_data: a dict mapping student username to athlete status info
    :return: an enriched dataset including athlete info for each student
    """
    result = []
    for row in student_data:
        new_row = row.copy()
        new_row['is_athlete'] = False
        try:
            new_row['athlete_sport'] = athlete_data[new_row['handshake_username'].upper()]
            new_row['is_athlete'] = True
            athlete_dept_row = new_row.copy()
            athlete_dept_row['department'] = Departments.SOAR_ATHLETICS.value.name
            result.append(athlete_dept_row)
        except KeyError:
            new_row['athlete_sport'] = None
        result.append(new_row)
    return result
