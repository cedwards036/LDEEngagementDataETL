from src.common import BrowsingSession, CONFIG
from src.events import transform_events_data, EVENTS_INSIGHTS_REPORT
from src.file_writer import write_engagement_data
from src.office_hours import transform_office_hours_data, APPT_INSIGHTS_REPORT

if __name__ == '__main__':
    with BrowsingSession() as browser:
        raw_appt_data = APPT_INSIGHTS_REPORT.extract_data(browser)
        clean_appt_data = transform_office_hours_data(raw_appt_data)

        raw_event_data = EVENTS_INSIGHTS_REPORT.extract_data(browser)
        clean_event_data = transform_events_data(raw_event_data)

        engagement_data = clean_appt_data + clean_event_data
        write_engagement_data(CONFIG['engagement_data_filepath'], engagement_data)
