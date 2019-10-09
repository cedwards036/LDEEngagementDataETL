from typing import List


class EducationDataRecord:

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
        return EducationDataRecord(self._data['major'], self._data['department'], self._data['college'])

    def __eq__(self, other: 'EducationDataRecord') -> bool:
        return self.to_dict() == other.to_dict()


class StudentDataRecord:

    def __init__(self, handshake_username: str = None, handshake_id: str = None,
                 email: str = None, first_name: str = None, pref_name: str = None,
                 last_name: str = None, school_year: str = None,
                 education_data: EducationDataRecord = None,
                 additional_departments: List[str] = None):
        self._data = {
            'handshake_username': handshake_username,
            'handshake_id': handshake_id,
            'email': email,
            'first_name': first_name,
            'pref_name': pref_name,
            'last_name': last_name,
            'school_year': school_year,
            'education_data': education_data,
            'additional_departments': additional_departments
        }
