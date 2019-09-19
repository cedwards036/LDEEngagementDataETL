from src.common import BrowsingSession, CONFIG
from src.events import run_events_etl
from src.file_writer import write_engagement_data
from src.office_hours import run_office_hours_etl

if __name__ == '__main__':
    with BrowsingSession() as browser:
        clean_appt_data = run_office_hours_etl(browser)
        clean_event_data = run_events_etl(browser)
        engagement_data = clean_appt_data + clean_event_data

        write_engagement_data(CONFIG['engagement_data_filepath'], engagement_data)
