from src.common import BrowsingSession, CONFIG
from src.events import run_events_etl
from src.file_writer import write_engagement_data, write_to_csv
from src.office_hours import run_office_hours_etl
from src.roster_data import run_students_etl

STUDENT_DATA_DIR = 'S:\\Reporting & Data\\Life Design Educator Engagement\\StudentData'
ROSTER_FILEPATHS = [
    f'{STUDENT_DATA_DIR}\\sis_undergrads_2019_09_20.csv',
]
HANDSHAKE_DATA_FILEPATH = f'{STUDENT_DATA_DIR}\\handshake_hwd_students_2019_09_16.csv'
MAJORS_FILEPATH = f'{STUDENT_DATA_DIR}\\all_majors_2019_09_18.csv'

if __name__ == '__main__':
    with BrowsingSession() as browser:
        clean_appt_data = run_office_hours_etl(browser)
        clean_event_data = run_events_etl(browser)
        engagement_data = clean_appt_data + clean_event_data
        write_engagement_data(CONFIG['engagement_data_filepath'], engagement_data)

    student_data = run_students_etl(ROSTER_FILEPATHS, HANDSHAKE_DATA_FILEPATH, MAJORS_FILEPATH)
    write_to_csv(CONFIG['student_data_filepath'], student_data)
