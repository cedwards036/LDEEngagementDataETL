from typing import List

from src.data_model import EngagementTypes, EngagementRecord
from src.satisfaction_survey_etl.survey_response import SurveyResponse


def transform_survey_data(raw_data: List[List[str]], event_data: List[EngagementRecord],
                          dept_conversion_dict: dict) -> List[SurveyResponse]:
    parsed_data = parse_raw_survey_data(raw_data)
    event_lookup = create_event_data_lookup(event_data)
    result = add_event_depts_to_survey_data(event_lookup, parsed_data)
    result = convert_office_hour_depts_in_survey_data(result, dept_conversion_dict)
    return result


def parse_raw_survey_data(raw_data: List[List[str]]) -> List[SurveyResponse]:
    return [_parse_raw_survey_data_row(row, row_index) for row_index, row in enumerate(raw_data)]


def _parse_raw_survey_data_row(row: List[str], row_index: int) -> SurveyResponse:
    def _get_nps_from_row(row: List[str]):
        return int(row[1])

    def _get_development_answer_from_row(row: List[str]):
        return row[2] == 'Yes'

    def _get_engagement_type_from_row(row: List[str]):
        if len(row) == 6:
            return EngagementTypes.OFFICE_HOURS.value
        elif len(row) == 7:
            return EngagementTypes.EVENT.value

    def _get_department_from_row(row: List[str]):
        if len(row) == 6:
            return row[5]
        else:
            return None

    def _get_event_id_from_row(row: List[str]):
        if len(row) > 6:
            return row[6]
        else:
            return None

    return SurveyResponse(
        response_id=str(row_index + 1),
        nps=_get_nps_from_row(row),
        experience_advanced_development=_get_development_answer_from_row(row),
        engagement_type=_get_engagement_type_from_row(row),
        office_hour_department=_get_department_from_row(row),
        event_id=_get_event_id_from_row(row)
    )


def create_event_data_lookup(event_data: List[EngagementRecord]) -> dict:
    return {row.data['handshake_engagement_id']: row.data['engagement_department'] for row in event_data}


def add_event_depts_to_survey_data(event_data: dict, survey_data: List[SurveyResponse]) -> List[SurveyResponse]:
    for response in survey_data:
        if response.event_id is not None:
            try:
                response.department = event_data[response.event_id]
            except KeyError:
                print(f'WARNING: Satisfaction survey event id "{response.event_id}" does not appear in Handshake data')
    return survey_data


def convert_office_hour_depts_in_survey_data(survey_data: List[SurveyResponse], conversion_dict: dict) -> List[SurveyResponse]:
    for response in survey_data:
        if response.office_hour_department is not None:
            try:
                response.department = conversion_dict[response.office_hour_department]
            except KeyError:
                raise ValueError(f'No match found for survey office hour department "{response.office_hour_department}"')
    return survey_data
