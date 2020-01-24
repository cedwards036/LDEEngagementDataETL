from typing import List

from autohandshake import HandshakeBrowser

from src.common import InsightsReport, parse_date_string, RangeInsightsDateField
from src.data_model import EngagementRecord, EngagementTypes, Mediums, Departments
from src.handshake_fields import CareerFairFields

CAREER_FAIRS_INSIGHTS_REPORT = InsightsReport(
    url='https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vY2FyZWVyX2ZhaXJfc2Vzc2lvbl9hdHRlbmRlZXM_cWlkPXlKVmZobzk5enFkY2pJMm42aHYxd0UmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9Zmls',
    date_field=RangeInsightsDateField(date_field_category='Career Fair Session',
                                      date_field_title='Session Start Date')
)


def run_career_fair_etl(browser: HandshakeBrowser) -> List[EngagementRecord]:
    """
    Run the full ETL process for career fair data

    :param browser: a logged-in HandshakeBrowser
    :return: a list consisting of cleaned career fair engagement data
    """
    raw_fair_data = CAREER_FAIRS_INSIGHTS_REPORT.extract_data(browser)
    return transform_fair_data(raw_fair_data)


def transform_fair_data(raw_fair_data: List[dict]) -> List[EngagementRecord]:
    """
    Transform raw career fair data into standard "engagement data" format

    :param raw_fair_data: raw career fair data from Handshake
    :return: cleaned career fair data in the form of "engagement data"
    """
    return [_transform_data_row(row) for row in raw_fair_data]


def _transform_data_row(raw_data_row: dict) -> EngagementRecord:
    return EngagementRecord(
        engagement_type=EngagementTypes.CAREER_FAIR,
        handshake_engagement_id=raw_data_row[CareerFairFields.ID],
        start_date_time=parse_date_string(
            raw_data_row[CareerFairFields.START_DATE_TIME]),
        medium=Mediums.IN_PERSON,
        engagement_name=raw_data_row[CareerFairFields.NAME],
        engagement_department=Departments.NO_DEPARTMENT.value,
        student_handshake_id=raw_data_row[CareerFairFields.STUDENT_ID],
        student_school_year_at_time_of_engagement=None,
        student_pre_registered=_student_pre_registered(raw_data_row),
        associated_staff_email=None
    )


def _student_pre_registered(raw_data_row: dict) -> bool:
    return raw_data_row[CareerFairFields.IS_PRE_REGISTERED] == 'Yes'
