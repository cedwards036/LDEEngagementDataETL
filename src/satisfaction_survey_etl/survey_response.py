from src.common import convert_empty_str_to_none


class SurveyResponse:

    def __init__(self, response_id: str = None, nps: int = None, experience_advanced_development: bool = None,
                 engagement_type: str = None, office_hour_department: str = None,
                 event_id: str = None, department: str = None):
        self._data = {
            'response_id': response_id,
            'nps': nps,
            'experience_advanced_development': experience_advanced_development,
            'engagement_type': engagement_type,
            'office_hour_department': convert_empty_str_to_none(office_hour_department),
            'event_id': convert_empty_str_to_none(event_id),
            'department': department
        }

    @property
    def event_id(self):
        return self._data['event_id']

    @property
    def office_hour_department(self):
        return self._data['office_hour_department']

    @property
    def department(self):
        return self._data['department']

    @department.setter
    def department(self, new_department: str):
        self._data['department'] = new_department


    def to_dict(self):
        return self._data.copy()

    def __eq__(self, other: 'SurveyResponse') -> bool:
        return self.to_dict() == other.to_dict()
