from collections import defaultdict
from typing import List

from src.common import read_csv
from src.data_model import Departments
from src.student_data_etl.student_data_record import EducationDataRecord


def run_data_file_etl(sis_roster_filepaths: List[str], handshake_data_filepath: str,
                      major_data_filepath: str, athlete_filepath: str) -> List[dict]:
    ALLOWED_FIELDS_FOR_DATA_FILE = [
        'handshake_id', 'handshake_username', 'department', 'college', 'major',
        'school_year', 'is_athlete', 'athlete_sport'
    ]
    major_data = _extract_major_data(major_data_filepath)
    athlete_data = _extract_athlete_data(athlete_filepath)
    student_data = run_students_etl(sis_roster_filepaths, handshake_data_filepath)
    return filter_list_of_dicts(enrich_with_athlete_data_for_data_file(
        enrich_with_dept_college_data_for_data_file(student_data, major_data), athlete_data),
        ALLOWED_FIELDS_FOR_DATA_FILE)


def run_roster_file_etl(sis_roster_filepaths: List[str], handshake_data_filepath: str,
                        major_data_filepath: str, athlete_filepath: str) -> List[dict]:
    ALLOWED_FIELDS_FOR_DATA_FILE = [
        'handshake_id', 'email', 'first_name', 'pref_name', 'last_name',
        'department', 'colleges', 'majors', 'school_year', 'is_athlete', 'athlete_sports'
    ]
    major_data = _extract_major_data(major_data_filepath)
    athlete_data = _extract_athlete_data(athlete_filepath)
    student_data = run_students_etl(sis_roster_filepaths, handshake_data_filepath)
    return filter_list_of_dicts(enrich_with_athlete_data_for_roster_file(
        enrich_with_dept_college_data_for_roster_file(student_data, major_data), athlete_data),
        ALLOWED_FIELDS_FOR_DATA_FILE)


def run_students_etl(sis_roster_filepaths: List[str], handshake_data_filepath: str) -> List[dict]:
    handshake_data = _extract_handshake_data(handshake_data_filepath)
    roster_data = _extract_sis_rosters(sis_roster_filepaths)
    return filter_handshake_data_with_sis_roster(handshake_data, roster_data)


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
    result = {}
    for row in raw_major_data:
        result[row['major']] = EducationDataRecord(
            major=row['major'],
            department=row['department'],
            college=row['college']
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


def filter_handshake_data_with_sis_roster(handshake_data: dict, sis_data: List[dict]) -> List[dict]:
    """
    Filter the given handshake data down to just those entries that appear in the SIS data.

    If a student in the SIS data cannot be found in the handshake data, raise an exception.
    """
    result = []
    for row in sis_data:
        try:
            new_row = handshake_data[row['handshake_username'].upper()].copy()
            new_row['handshake_username'] = row['handshake_username']
            result.append(new_row)
        except KeyError:
            raise ValueError(f'No match found for user "{row["handshake_username"]}"')
    return result


def get_major_dept_college_data(student_data: dict, dept_college_data: dict) -> List[EducationDataRecord]:
    """
    Given a row of student data and a major-dept-college lookup dict, produce a
    list of major-dept-college data relevant to that student.
    """

    def _look_up_dept_college_data(major: str) -> EducationDataRecord:
        try:
            result = dept_college_data[major].copy()
            result.major = _clean_major(result.major)
            return result
        except KeyError:
            raise ValueError(f'Unknown major "{major}"')

    def _create_fye_copy(education_data_record: EducationDataRecord) -> EducationDataRecord:
        result = education_data_record.copy()
        if education_data_record.college == 'wse':
            result.department = Departments.SOAR_FYE_WSE.value.name
        elif education_data_record.college == 'ksas':
            result.department = Departments.SOAR_FYE_KSAS.value.name
        return result

    def _is_masters_degree(major: str) -> bool:
        masters_prefixes = ['M.S.E.', 'M.A.', 'M.S.', 'M.F.A']
        for prefix in masters_prefixes:
            if major.startswith(prefix):
                return True
        return False

    def _clean_major(major: str) -> str:
        colon_loc = major.find(':')
        if colon_loc == -1 or _is_masters_degree(major):
            return major
        else:
            return major[colon_loc + 1:].strip()

    FYE_DEPTS = [Departments.SOAR_FYE_WSE.value.name, Departments.SOAR_FYE_KSAS.value.name]
    if not student_data['majors'] or student_data['majors'] == ['']:
        return [EducationDataRecord()]
    else:
        result = []
        for major in student_data['majors']:
            if 'interdisciplinary studies' in major.lower():
                return [EducationDataRecord(major=major)]
            else:
                data_row = _look_up_dept_college_data(major)
                result.append(data_row)
                if student_data['school_year'] == 'Freshman' and data_row.department not in FYE_DEPTS:
                    result.append(_create_fye_copy(data_row))
        return result


def enrich_with_dept_college_data_for_data_file(student_data: List[dict], dept_college_data: dict) -> List[dict]:
    """
    Enrich student data with appropriate department affiliation and college data.

    :param student_data: student data with 'major' and 'school_year' fields
    :param dept_college_data: a dict mapping username to dept and college data
    :return: an enriched dataset including department affiliations and colleges for each student
    """
    result = []
    for student_row in student_data:
        for data_row in get_major_dept_college_data(student_row, dept_college_data):
            result_row = student_row.copy()
            result_row.update(data_row.to_dict())
            del result_row['majors']
            result.append(result_row)
    return result


def enrich_with_dept_college_data_for_roster_file(student_data: List[dict], dept_college_data: dict) -> List[dict]:
    """
    Enrich student data with appropriate department affiliation and college data.

    :param student_data: student data with 'major' and 'school_year' fields
    :param dept_college_data: a dict mapping username to dept and college data
    :return: an enriched dataset including department affiliations and colleges for each student
    """

    def _get_uniques_from_field(education_data_records: List[EducationDataRecord], field: str) -> List[str]:
        education_data_dicts = [record.to_dict() for record in education_data_records]
        result = list(dict.fromkeys([row[field] for row in education_data_dicts]))
        if result == [None]:
            return []
        else:
            return result

    result = []
    for student_row in student_data:
        supplemental_data = get_major_dept_college_data(student_row, dept_college_data)
        majors_str = '; '.join(_get_uniques_from_field(supplemental_data, 'major'))
        colleges_str = '; '.join(_get_uniques_from_field(supplemental_data, 'college'))
        departments = _get_uniques_from_field(supplemental_data, 'department')
        for department in departments:
            result_row = student_row.copy()
            result_row['department'] = department
            result_row['majors'] = majors_str
            result_row['colleges'] = colleges_str
            result.append(result_row)
    return result


class AthleteUsernameUsageRecorder:
    def __init__(self):
        self._data = defaultdict(int)

    def record_usage(self, username: str):
        self._data[username] += 1

    def username_is_not_fully_processed(self, username: str, expected_count: int):
        return self._data[username] < expected_count


def create_athlete_data_enricher(add_sport_data_func: callable, process_row_func: callable) -> callable:
    def _create_athlete_row_copy(row: dict) -> dict:
        new_row = row.copy()
        new_row['is_athlete'] = True
        return new_row

    def _create_non_athlete_row_copy(row: dict) -> dict:
        new_row = row.copy()
        new_row['is_athlete'] = False
        return new_row

    def _create_soar_athletics_row(row: dict) -> dict:
        soar_athletics_row = row.copy()
        soar_athletics_row['department'] = Departments.SOAR_ATHLETICS.value.name
        return soar_athletics_row

    def _get_enriched_data_from_row(row: dict, usage_recorder: AthleteUsernameUsageRecorder,
                                    usage_limit: int, sport_data) -> List[dict]:
        result = []
        new_row = _create_athlete_row_copy(row)
        new_row = add_sport_data_func(new_row, sport_data)
        result.append(new_row)
        if usage_recorder.username_is_not_fully_processed(new_row['handshake_username'], usage_limit):
            result.append(_create_soar_athletics_row(new_row))
            usage_recorder.record_usage(row['handshake_username'])
        return result

    def enricher_func(student_data: List[dict], athlete_data: dict) -> List[dict]:
        result = []
        username_usage_recorder = AthleteUsernameUsageRecorder()
        for row in student_data:
            try:
                result += process_row_func(row, athlete_data, username_usage_recorder,
                                           _get_enriched_data_from_row)
            except KeyError:
                new_row = _create_non_athlete_row_copy(row)
                new_row = add_sport_data_func(new_row, sport_data=None)
                result.append(new_row)
        return result

    return enricher_func


def enrich_with_athlete_data_for_data_file(student_data: List[dict], athlete_data: dict) -> List[dict]:
    """
    Enrich student data with student athlete status in preparation for dashboard data file output.

    :param student_data: student data with a 'handshake_username' field
    :param athlete_data: a dict mapping student username to athlete status info
    :return: an enriched dataset including athlete info for each student
    """

    def _add_sport_data_to_row(row: dict, sport_data) -> dict:
        row['athlete_sport'] = sport_data
        return row

    def _process_row(row: dict, athlete_data: dict, usage_recorder: AthleteUsernameUsageRecorder,
                     row_enrichment_func: callable) -> List[dict]:
        result = []
        sports = athlete_data[row['handshake_username'].upper()]
        for sport_data in sports:
            result += row_enrichment_func(row, usage_recorder, len(sports), sport_data)
        return result

    data_enricher = create_athlete_data_enricher(_add_sport_data_to_row, _process_row)
    return data_enricher(student_data, athlete_data)


def enrich_with_athlete_data_for_roster_file(student_data: List[dict], athlete_data: dict) -> List[dict]:
    """
    Enrich student data with student athlete status in preparation for roster file output.

    :param student_data: student data with a 'handshake_username' field
    :param athlete_data: a dict mapping student username to athlete status info
    :return: an enriched dataset including athlete info for each student
    """

    def _add_sport_data_to_row(row: dict, sport_data) -> dict:
        if not sport_data:
            row['athlete_sports'] = None
        else:
            row['athlete_sports'] = '; '.join(sport_data)
        return row

    def _process_row(row: dict, athlete_data: dict, usage_recorder: AthleteUsernameUsageRecorder,
                     row_enrichment_func: callable) -> List[dict]:
        sport_data = athlete_data[row['handshake_username'].upper()]
        return row_enrichment_func(row, usage_recorder, 1, sport_data)

    data_enricher = create_athlete_data_enricher(_add_sport_data_to_row, _process_row)
    return data_enricher(student_data, athlete_data)


def filter_list_of_dicts(list_of_dicts: List[dict], allowed_fields: list) -> List[dict]:
    return [filter_dict(d, allowed_fields) for d in list_of_dicts]


def filter_dict(dic: dict, allowed_fields: list) -> dict:
    return {k: dic[k] for k in allowed_fields}
