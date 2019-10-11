from typing import List

from src.common import read_csv
from src.data_model import Departments
from src.student_data_etl.output_formatters import format_for_roster_file, format_for_data_file
from src.student_data_etl.student_data_record import EducationRecord, StudentRecord


def create_student_output_etl_function(formatter: callable) -> callable:
    """
    Create a function that runs the student data file ETL process and applies a
    formatter function to the result.

    :param formatter: the formatter function to apply to the student data
    :return: a formatted dataset, ready for outputting to a file
    """

    def run_etl(sis_roster_filepaths: List[str], handshake_data_filepath: str,
                        major_data_filepath: str, athlete_filepath: str) -> List[dict]:
        handshake_data = _extract_handshake_data(handshake_data_filepath)
        sis_data = _extract_sis_rosters(sis_roster_filepaths)
        major_data = _extract_major_data(major_data_filepath)
        athlete_data = _extract_athlete_data(athlete_filepath)
        return formatter(
            enrich_with_athlete_status(
                enrich_with_dept_college_data(
                    filter_handshake_data_with_sis_roster(
                        handshake_data, sis_data
                    ),
                    major_data
                ),
                athlete_data
            )
        )

    return run_etl


run_roster_file_etl = create_student_output_etl_function(format_for_roster_file)
run_data_file_etl = create_student_output_etl_function(format_for_data_file)


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
        result[row['major']] = EducationRecord(
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


def get_major_dept_college_data(student_data: dict, dept_college_data: dict) -> List[EducationRecord]:
    """
    Given a row of student data and a major-dept-college lookup dict, produce a
    list of major-dept-college data relevant to that student.
    """

    def _look_up_dept_college_data(major: str) -> EducationRecord:
        try:
            result = dept_college_data[major].copy()
            result.major = _clean_major(result.major)
            return result
        except KeyError:
            raise ValueError(f'Unknown major "{major}"')

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

    if not student_data['majors'] or student_data['majors'] == ['']:
        return [EducationRecord()]
    else:
        result = []
        for major in student_data['majors']:
            if 'interdisciplinary studies' in major.lower():
                return [EducationRecord(major=major)]
            else:
                data_row = _look_up_dept_college_data(major)
                result.append(data_row)
        return result


def enrich_with_dept_college_data(student_data: List[dict], dept_college_data: dict) -> List[StudentRecord]:
    """
    Enrich student data with appropriate department affiliation and college data.

    :param student_data: student data with 'major' and 'school_year' fields
    :param dept_college_data: a dict mapping username to dept and college data
    :return: an enriched dataset including department affiliations and colleges for each student
    """
    result = []
    for student_row in student_data:
        student_record = StudentRecord(
            handshake_username=student_row['handshake_username'],
            handshake_id=student_row['handshake_id'],
            email=student_row['email'],
            first_name=student_row['first_name'],
            pref_name=student_row['pref_name'],
            last_name=student_row['last_name'],
            school_year=student_row['school_year']
        )
        for education_record in get_major_dept_college_data(student_row, dept_college_data):
            student_record.add_education_record(education_record)
        if student_record.school_year == 'Freshman':
            if 'wse' in student_record.colleges and Departments.SOAR_FYE_WSE.value.name not in student_record.departments:
                student_record.add_additional_department(Departments.SOAR_FYE_WSE.value.name)
            if 'ksas' in student_record.colleges and Departments.SOAR_FYE_KSAS.value.name not in student_record.departments:
                student_record.add_additional_department(Departments.SOAR_FYE_KSAS.value.name)
        result.append(student_record)
    return result


def enrich_with_athlete_status(student_data: List[StudentRecord], athlete_data: dict) -> List[StudentRecord]:
    """
    Enrich a list of Student Records with their athlete statuses.

    :param student_data: the student data to enrich
    :param athlete_data: a dictionary mapping students to their athlete status
    :return: an enrich list of student records containing athlete data
    """
    for record in student_data:
        try:
            sports = athlete_data[record.handshake_username.upper()]
            for sport in sports:
                record.add_sport(sport)
        except KeyError:
            pass  # do nothing if student has no athlete data
    return student_data
