from typing import List, Union

from src.common import convert_none_to_empty_str
from src.student_data_etl.student_data_record import StudentRecord, EducationRecord


def _prep_formatted_record_copy(student_record: StudentRecord, result_fields: List[str]) -> dict:
    def _remove_none_from_student_record_dict(student_record_dict: dict) -> dict:
        for key in student_record_dict.keys():
            student_record_dict[key] = convert_none_to_empty_str(student_record_dict[key])
        return student_record_dict

    result = student_record.to_dict(result_fields)
    return _remove_none_from_student_record_dict(result)


def format_for_roster_file(student_records: List[StudentRecord]) -> List[dict]:
    """
    Format student records for outputting to a multi-tab LDE Roster excel file
    """
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

    result_fields = ['handshake_id', 'email', 'first_name', 'pref_name', 'last_name',
                     'school_year', 'is_athlete', 'sports', 'majors', 'colleges']
    result = []
    for student_record in student_records:
        if student_record.departments:
            for department in student_record.departments:
                result.append(_create_full_formatted_record(student_record, department, result_fields))
        elif student_record.majors:
            result.append(_create_full_formatted_record(student_record, None, result_fields))
        else:  # record has no enrichment data
            result.append(_create_blank_formatted_record(student_record, result_fields))
    return result


def format_for_data_file(student_records: List[StudentRecord]) -> List[dict]:
    """
    Format student records for outputting to a data-analysis-friendly csv
    """

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

    def _create_formatted_records(student_record: StudentRecord, education_record: EducationRecord = None) -> List[dict]:
        result = []
        departments = student_record.additional_departments
        if education_record is None:
            education_record = EducationRecord()
        else:
            departments.append(education_record.department)
        for department in departments:
            if student_record.sports:
                for sport in student_record.sports:
                    result.append(_create_formatted_record(student_record, result_fields, RowSpecificData(major=education_record.major,
                                                                                                          department=department,
                                                                                                          college=education_record.college,
                                                                                                          sport=sport)))
            else:
                result.append(_create_formatted_record(student_record, result_fields, RowSpecificData(major=education_record.major,
                                                                                                      department=department,
                                                                                                      college=education_record.college)))
        return result

    def _create_formatted_record(student_record: StudentRecord, result_fields: List[str],
                                 row_specific_data: RowSpecificData) -> dict:
        result_record = _prep_formatted_record_copy(student_record, result_fields)
        result_record.update(row_specific_data.data)
        return result_record

    result_fields = ['handshake_username', 'handshake_id', 'school_year', 'is_athlete']

    result = []
    for student_record in student_records:
        if student_record.education_records:
            for education_record in student_record.education_records:
                result += _create_formatted_records(student_record, education_record)
        elif student_record.additional_departments:
            result += _create_formatted_records(student_record)
        else:  # record has no enrichment data
            result.append(_create_formatted_record(student_record, result_fields, RowSpecificData()))
    return result
