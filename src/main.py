from src.common import BrowsingSession, CONFIG
from src.engagement_data_etl.career_fairs import run_career_fair_etl
from src.engagement_data_etl.events import run_events_etl
from src.engagement_data_etl.interviews import run_interviews_etl
from src.engagement_data_etl.office_hours import run_office_hours_etl
from src.file_writers import write_engagement_data, write_to_csv, write_roster_excel_file
from src.satisfaction_survey_etl.etl_processes import run_survey_etl
from src.student_data_etl.etl_processes import run_data_file_etl, run_roster_file_etl
from src.student_data_etl.extractors import extract_handshake_data

STUDENT_DATA_DIR = 'S:\\Reporting & Data\\Life Design Educator Engagement\\StudentData'
MAJORS_FILEPATH = f'{STUDENT_DATA_DIR}\\all_majors.csv'
ATHLETE_FILEPATH = f'{STUDENT_DATA_DIR}\\student_athlete_roster_2020_01_24.csv'

if __name__ == '__main__':
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
        print('Pulling Handshake student data...')
        handshake_data = extract_handshake_data(browser)

    student_data = run_data_file_etl(handshake_data, MAJORS_FILEPATH, ATHLETE_FILEPATH)
    roster_data = run_roster_file_etl(handshake_data, MAJORS_FILEPATH, ATHLETE_FILEPATH)
    print('Writing student roster data...')
    write_to_csv(CONFIG['student_data_filepath'], student_data)
    write_roster_excel_file(CONFIG['student_roster_filepath'], roster_data)

    print('Pulling satisfaction survey data...')
    survey_data = run_survey_etl(clean_event_data)
    print('Writing satisfaction survey data')
    write_to_csv(CONFIG['survey_data_filepath'], survey_data)

    print('Complete!')
