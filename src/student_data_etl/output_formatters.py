from typing import List, Union

from src.common import convert_none_to_empty_str
from src.student_data_etl.student_data_record import StudentRecord, EducationRecord


def _prep_formatted_record_copy(student_record: StudentRecord, result_fields: List[str]) -> dict:
    result = student_record.to_dict(result_fields)
    return {key: convert_none_to_empty_str(value) for key, value in result.items()}


def format_student_records_for_roster_file(student_records: List[StudentRecord]) -> List[dict]:
    def _list_to_str(lst: List[str]):
        return '; '.join(lst)

    def _create_full_formatted_record(student_record: StudentRecord, department: Union[str, None],
                                      result_fields: List[str]) -> dict:
        result_record = _prep_formatted_record_copy(student_record, result_fields)
        result_record['sports'] = _list_to_str(student_record.sports)
        result_record['colleges'] = _list_to_str(student_record.colleges)
        result_record['majors'] = _list_to_str(student_record.majors)
        if department is None:
            result_record['department'] = ''
        else:
            result_record['department'] = department
        return result_record

    def _create_blank_formatted_record(student_record: StudentRecord, result_fields: List[str]) -> dict:
        result_record = _prep_formatted_record_copy(student_record, result_fields)
        result_record['sports'] = ''
        result_record['colleges'] = ''
        result_record['department'] = ''
        result_record['majors'] = ''
        return result_record

    def _add_department_records_to_result(result_fields: List[str], student_record: StudentRecord) -> List[dict]:
        result = []
        for department in student_record.departments:
            result.append(_create_full_formatted_record(student_record, department, result_fields))
        return result

    def _create_formatted_records_from_raw_student_record(result_fields: List[str], student_record: StudentRecord) -> List[dict]:
        if student_record.departments:
            return _add_department_records_to_result(result_fields, student_record)
        elif student_record.majors:
            return [_create_full_formatted_record(student_record, None, result_fields)]
        else:  # record has no enrichment data
            return [_create_blank_formatted_record(student_record, result_fields)]

    result_fields = ['handshake_id', 'email', 'first_name', 'legal_first_name',
                     'pref_first_name', 'last_name', 'school_year', 'is_athlete',
                     'sports', 'majors', 'colleges', 'is_pre_med',
                     'has_activated_handshake', 'has_completed_profile']
    result = []
    for student_record in student_records:
        result += _create_formatted_records_from_raw_student_record(result_fields, student_record)
    return result


class _DataFileRecordFormatter:

    def __init__(self, student_record: StudentRecord):
        self._student_record = student_record
        self._result_fields = ['handshake_username', 'handshake_id', 'school_year',
                               'is_pre_med', 'has_activated_handshake', 'has_completed_profile',
                               'is_athlete']

    def format(self) -> List[dict]:
        if self._student_record.education_records:
            return self._create_formatted_records_from_education_data()
        elif self._student_record.additional_departments:
            return self._create_formatted_records(EducationRecord())
        else:  # record has no enrichment data
            return [self._create_formatted_record(self.RowSpecificData())]

    def _create_formatted_records_from_education_data(self):
        result = []
        for education_record in self._student_record.education_records:
            result += self._create_formatted_records(education_record)
        return result

    def _create_formatted_records(self, education_record: EducationRecord) -> List[dict]:
        result = []
        departments = self._get_department_list(education_record)
        for department in departments:
            result += self._create_formatted_records_for_department(department, education_record)
        return result

    def _get_department_list(self, education_record: EducationRecord):
        departments = self._student_record.additional_departments
        if (education_record.department is not None) or (not departments):
            departments.append(education_record.department)
        return departments

    def _create_formatted_records_for_department(self, department: str, education_record: EducationRecord):
        if self._student_record.sports:
            return self._create_formatted_records_with_sports_data(department, education_record)
        else:
            return self._create_formatted_records_with_no_sports_data(department, education_record)

    def _create_formatted_records_with_sports_data(self, department: str, education_record: EducationRecord):
        return [
            self._create_formatted_record(
                self.RowSpecificData(major=education_record.major,
                                     department=department,
                                     college=education_record.college,
                                     sport=sport)
            ) for sport in self._student_record.sports
        ]

    def _create_formatted_records_with_no_sports_data(self, department: str, education_record: EducationRecord):
        return [self._create_formatted_record(self.RowSpecificData(major=education_record.major,
                                                                   department=department,
                                                                   college=education_record.college))]

    def _create_formatted_record(self, row_specific_data: 'RowSpecificData') -> dict:
        result_record = _prep_formatted_record_copy(self._student_record, self._result_fields)
        result_record.update(row_specific_data.data)
        return result_record

    class RowSpecificData:

        def __init__(self, major: str = '', department: str = '', college: str = '', sport: str = ''):
            self._data = {
                'major': convert_none_to_empty_str(major),
                'department': convert_none_to_empty_str(department),
                'college': convert_none_to_empty_str(college),
                'sport': convert_none_to_empty_str(sport)
            }

        @property
        def data(self) -> dict:
            return self._data.copy()


def format_student_records_for_data_file(student_records: List[StudentRecord]) -> List[dict]:
    result = []
    for student_record in student_records:
        result += _DataFileRecordFormatter(student_record).format()
    return result
