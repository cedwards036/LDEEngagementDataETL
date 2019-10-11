from typing import List

from src.data_model import Departments
from src.student_data_etl.student_data_record import StudentRecord, EducationRecord


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


def enrich_with_education_records(student_data: List[dict], education_data: dict) -> List[StudentRecord]:
    """
    Enrich student data with appropriate education data, including department and college.

    :param student_data: student data with 'major' and 'school_year' fields
    :param education_data: a dict mapping username to education records
    :return: an enriched dataset including department affiliations and colleges for each student
    """

    def _add_freshman_depts(student_record: StudentRecord) -> StudentRecord:
        if 'wse' in student_record.colleges and Departments.SOAR_FYE_WSE.value.name not in student_record.departments:
            student_record.add_additional_department(Departments.SOAR_FYE_WSE.value.name)
        if 'ksas' in student_record.colleges and Departments.SOAR_FYE_KSAS.value.name not in student_record.departments:
            student_record.add_additional_department(Departments.SOAR_FYE_KSAS.value.name)
        return student_record

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
        for education_record in get_education_records_for_student(student_row, education_data):
            student_record.add_education_record(education_record)
        if student_record.school_year == 'Freshman':
            student_record = _add_freshman_depts(student_record)
        result.append(student_record)
    return result


def get_education_records_for_student(student_data: dict, dept_college_data: dict) -> List[EducationRecord]:
    """
    Given a row of student data and a major-dept-college lookup dict, produce a
    list of education records relevant to that student.
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
                result.append(EducationRecord(major=_clean_major(major)))
            else:
                data_row = _look_up_dept_college_data(major)
                result.append(data_row)
        return result
