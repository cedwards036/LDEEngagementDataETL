from src.common import BrowsingSession, CONFIG
from src.engagement_data_etl.career_fairs import run_career_fair_etl
from src.engagement_data_etl.events import run_events_etl
from src.engagement_data_etl.interviews import run_interviews_etl
from src.engagement_data_etl.office_hours import run_office_hours_etl
from src.file_writers import write_engagement_data


def run_engagement_etl():
    with BrowsingSession() as browser:
        print('Pulling office hour data...')
        clean_appt_data = run_office_hours_etl(browser)
        print('Pulling event data...')
        clean_event_data = run_events_etl(browser)
        print('Pulling career fair data...')
        clean_fair_data = run_career_fair_etl(browser)
        print('Pulling interview data...')
        clean_interview_data = run_interviews_etl(browser)
        print('Writing engagement data...')
        engagement_data = clean_appt_data + clean_event_data + clean_fair_data + clean_interview_data
        write_engagement_data(CONFIG['engagement_data_filepath'], engagement_data)


if __name__ == '__main__':
    run_engagement_etl()
