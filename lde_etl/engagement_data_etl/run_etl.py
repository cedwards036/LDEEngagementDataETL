from lde_etl.common import BrowsingSession
from lde_etl.engagement_data_etl.career_fairs import run_career_fair_etl
from lde_etl.engagement_data_etl.events import run_events_etl
from lde_etl.engagement_data_etl.interviews import run_interviews_etl
from lde_etl.engagement_data_etl.office_hours import run_office_hours_etl
from lde_etl.file_writers import write_engagement_data


def run_engagement_etl(config):
    with BrowsingSession(config) as browser:
        print('Pulling office hour data...')
        clean_appt_data = run_office_hours_etl(browser, config['download_dir'])
        print('Pulling event data...')
        clean_event_data = run_events_etl(browser, config['download_dir'])
        print('Pulling career fair data...')
        clean_fair_data = run_career_fair_etl(browser, config['download_dir'])
        print('Pulling interview data...')
        clean_interview_data = run_interviews_etl(browser, config['download_dir'])
        print('Writing engagement data...')
        engagement_data = clean_appt_data + clean_event_data + clean_fair_data + clean_interview_data
        write_engagement_data(config['engagement_data_filepath'], engagement_data)
