from typing import List, Union
from src.student_data_etl.student_data_record import StudentRecord

def format_for_roster_file(student_records: List[StudentRecord]) -> List[dict]:

    def _list_to_str(lst: List[str]):
        return '; '.join(lst)

    def _create_full_formatted_record(student_record: StudentRecord, department: Union[str, None],
                                      result_fields: List[str]) -> dict:
        result_record = student_record.to_dict(result_fields)
        result_record = _convert_none_to_empty_str(result_record)
        result_record['sports'] = _list_to_str(student_record.sports)
        result_record['colleges'] = _list_to_str(student_record.colleges)
        result_record['majors'] = _list_to_str(student_record.majors)
        if department is None:
            result_record['department'] = ''
        else:
            result_record['department'] = department
        return result_record

    def _create_blank_formatted_record(student_record: StudentRecord, result_fields: List[str]) -> dict:
        result_record = student_record.to_dict(result_fields)
        result_record = _convert_none_to_empty_str(result_record)
        result_record['sports'] = ''
        result_record['colleges'] = ''
        result_record['department'] = ''
        result_record['majors'] = ''
        return result_record

    def _convert_none_to_empty_str(student_record_dict: dict) -> dict:
        for key in student_record_dict.keys():
            if student_record_dict[key] is None:
                student_record_dict[key] = ''
        return student_record_dict

    result_fields = ['handshake_id', 'email', 'first_name', 'pref_name', 'last_name',
                     'school_year', 'is_athlete', 'sports', 'majors', 'colleges']
    result = []
    for student_record in student_records:
        if student_record.departments:
            for department in student_record.departments:
                result.append(_create_full_formatted_record(student_record, department, result_fields))
        elif student_record.majors:
            result.append(_create_full_formatted_record(student_record, None, result_fields))
        else: # record has no enrichment data
            result.append(_create_blank_formatted_record(student_record, result_fields))
    return result