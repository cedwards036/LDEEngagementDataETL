from src.common import convert_empty_str_to_none


class SurveyResponse:

    def __init__(self, nps: int = None, experience_advanced_development: bool = None,
                 office_hour_department: str = None, event_id: str = None):
        self._data = {
            'nps': nps,
            'experience_advanced_development': experience_advanced_development,
            'office_hour_department': convert_empty_str_to_none(office_hour_department),
            'event_id': convert_empty_str_to_none(event_id)
        }

    def to_dict(self):
        return self._data.copy()

    def __eq__(self, other: 'SurveyResponse') -> bool:
        return self.to_dict() == other.to_dict()
