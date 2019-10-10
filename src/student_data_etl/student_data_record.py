import copy
from typing import List

from src.data_model import Departments


class EducationRecord:

    def __init__(self, major: str = None, department: str = None, college: str = None):
        self._data = {
            'major': major,
            'department': department,
            'college': college
        }

    def to_dict(self) -> dict:
        return self._data.copy()

    @property
    def major(self) -> str:
        return self._data['major']

    @property
    def department(self) -> str:
        return self._data['department']

    @property
    def college(self) -> str:
        return self._data['college']

    @major.setter
    def major(self, new_major: str):
        self._data['major'] = new_major

    @department.setter
    def department(self, new_dept: str):
        self._data['department'] = new_dept

    def copy(self):
        return EducationRecord(self._data['major'], self._data['department'], self._data['college'])

    def __eq__(self, other: 'EducationRecord') -> bool:
        return self.to_dict() == other.to_dict()

    def __str__(self):
        return str(self.to_dict())


class StudentRecord:

    def __init__(self, handshake_username: str = None, handshake_id: str = None,
                 email: str = None, first_name: str = None, pref_name: str = None,
                 last_name: str = None, school_year: str = None,
                 education_data: List[EducationRecord] = None,
                 additional_departments: List[str] = None, sports: List[str] = None):

        self._data = {
            'handshake_username': self._convert_empty_str_to_none(handshake_username),
            'handshake_id': self._convert_empty_str_to_none(handshake_id),
            'email': self._convert_empty_str_to_none(email),
            'first_name': self._convert_empty_str_to_none(first_name),
            'pref_name': self._convert_empty_str_to_none(pref_name),
            'last_name': self._convert_empty_str_to_none(last_name),
            'school_year': self._convert_empty_str_to_none(school_year),
            'education_records': [],
            'additional_departments': [],
            'is_athlete': False,
            'sports': [],
            'majors': [],
            'colleges': [],
            'departments': []
        }
        if education_data:
            for record in education_data:
                self.add_education_record(record)
        if additional_departments:
            for department in additional_departments:
                self.add_additional_department(department)
        if sports:
            for sport in sports:
                self.add_sport(sport)

    @property
    def handshake_username(self) -> str:
        return self._data['handshake_username']

    @property
    def education_records(self):
        return copy.deepcopy(self._data['education_records'])

    @property
    def colleges(self) -> List[str]:
        return self._data['colleges'].copy()

    @property
    def majors(self) -> List[str]:
        return self._data['majors'].copy()

    @property
    def departments(self) -> List[str]:
        return self._data['departments'].copy()

    @property
    def additional_departments(self) -> List[str]:
        return self._data['additional_departments'].copy()

    @property
    def is_athlete(self) -> bool:
        return self._data['is_athlete']

    @property
    def sports(self) -> List[str]:
        return self._data['sports'].copy()

    def to_dict(self, fields: List[str] = None) -> dict:
        result = copy.deepcopy(self._data)
        if fields is not None:
            result = {field: result[field] for field in fields}
        return result

    def add_education_record(self, record: EducationRecord):
        self._add_value_to_unique_list(record, self._data['education_records'])
        self._update_colleges_with_education_record(record)
        self._update_majors_with_education_record(record)
        self._update_depts_with_education_record(record)

    def add_additional_department(self, department: str):
        self._add_value_to_unique_list(department, self._data['additional_departments'])
        self._add_value_to_unique_list(department, self._data['departments'])

    def add_sport(self, sport: str):
        self._data['is_athlete'] = True
        self._add_value_to_unique_list(sport, self._data['sports'])
        self.add_additional_department(Departments.SOAR_ATHLETICS.value.name)

    def _update_colleges_with_education_record(self, education_data_record: EducationRecord):
        if education_data_record.college is not None:
            self._add_value_to_unique_list(education_data_record.college, self._data['colleges'])

    def _update_majors_with_education_record(self, education_data_record: EducationRecord):
        if education_data_record.major is not None:
            self._add_value_to_unique_list(education_data_record.major, self._data['majors'])

    def _update_depts_with_education_record(self, education_data_record: EducationRecord):
        if education_data_record.department is not None:
            self._add_value_to_unique_list(education_data_record.department, self._data['departments'])

    @staticmethod
    def _add_value_to_unique_list(value, unique_list: list):
        if value not in unique_list:
            unique_list.append(value)

    @staticmethod
    def _convert_empty_str_to_none(value: str):
        if value == '':
            return None
        else:
            return value

    def __eq__(self, other: 'StudentRecord'):
        return self.to_dict() == other.to_dict()

    def __str__(self):
        printable_dict = self.to_dict()
        printable_dict['education_records'] = [str(record) for record in printable_dict['education_records']]
        return str(printable_dict)
