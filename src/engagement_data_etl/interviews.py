from typing import List

from autohandshake import HandshakeBrowser

from src.common import InsightsReport, parse_date_string, RangeInsightsDateField
from src.data_model import EngagementRecord, EngagementTypes, Mediums, Departments
from src.handshake_fields import InterviewFields

INTERVIEWS_INSIGHTS_REPORT = InsightsReport(
    url='https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vaW50ZXJ2aWV3X3NjaGVkdWxlcz9xaWQ9UXQ1OTFORFhJaWZ5MG9FdlMyUURYQiZlbWJlZF9kb21haW49aHR0cHM6JTJGJTJGYXBwLmpvaW5oYW5kc2hha2UuY29tJnRvZ2dsZT1maWw=',
    date_field=RangeInsightsDateField(date_field_category='Interview Schedule Dates',
                                      date_field_title='Date Date')
)


def run_interviews_etl(browser: HandshakeBrowser) -> List[EngagementRecord]:
    """
    Run the full ETL process for events data

    :param browser: a logged-in HandshakeBrowser
    :return: a list consisting of cleaned event engagement data
    """
    raw_event_data = INTERVIEWS_INSIGHTS_REPORT.extract_data(browser)
    return transform_interviews_data(raw_event_data)


def transform_interviews_data(raw_interview_data: List[dict]) -> List[EngagementRecord]:
    return [_transform_data_row(row) for row in raw_interview_data]


def _transform_data_row(raw_data_row: dict) -> EngagementRecord:
    return EngagementRecord(
        engagement_type=EngagementTypes.INTERVIEW,
        handshake_engagement_id=raw_data_row[InterviewFields.ID],
        start_date_time=parse_date_string(raw_data_row[InterviewFields.DATE_TIME]),
        medium=Mediums.IN_PERSON,
        engagement_name=_make_engagement_name(raw_data_row),
        engagement_department=Departments.NO_DEPARTMENT.value,
        student_handshake_id=raw_data_row[InterviewFields.STUDENT_ID],
        student_school_year_at_time_of_engagement=None,
        student_pre_registered=True,
        associated_staff_email=None
    )


def _make_engagement_name(raw_data_row: dict) -> str:
    return f'{raw_data_row[InterviewFields.EMPLOYER]} Interviews on {format_list(raw_data_row[InterviewFields.DATE_LIST])}'


def format_list(list_str: str) -> str:
    items = list_str.split(', ')
    if len(items) < 2:
        return list_str
    elif len(items) == 2:
        return f'{items[0]} and {items[1]}'
    else:
        return ', '.join(items[:-1]) + ', and ' + items[-1]
