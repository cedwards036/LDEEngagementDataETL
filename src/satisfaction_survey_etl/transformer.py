from typing import List

from src.satisfaction_survey_etl.survey_response import SurveyResponse


def transform_survey_data(raw_data: List[List[str]]) -> List[SurveyResponse]:
    return [_transform_survey_data_row(row) for row in raw_data]


def _transform_survey_data_row(row: List[str]) -> SurveyResponse:
    def _get_nps_from_row(row: List[str]):
        return int(row[1])

    def _get_development_answer_from_row(row: List[str]):
        return row[2] == 'Yes'

    def _get_department_from_row(row: List[str]):
        if len(row) > 5:
            return row[5]
        else:
            return None

    def _get_event_id_from_row(row: List[str]):
        if len(row) > 6:
            return row[6]
        else:
            return None

    return SurveyResponse(
        nps=_get_nps_from_row(row),
        experience_advanced_development=_get_development_answer_from_row(row),
        office_hour_department=_get_department_from_row(row),
        event_id=_get_event_id_from_row(row)
    )
