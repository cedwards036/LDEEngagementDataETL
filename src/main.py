from src.common import BrowsingSession, CONFIG
from src.engagement_data_etl.career_fairs import run_career_fair_etl
from src.engagement_data_etl.events import run_events_etl
from src.engagement_data_etl.office_hours import run_office_hours_etl
from src.file_writers import write_engagement_data, write_to_csv, write_roster_excel_file
from src.student_data_etl.etl_processes import run_data_file_etl, run_roster_file_etl

# handshake data url: https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPTdZa0VnSW5RQ1J2aGNBWE9PcXgyVkUmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9Zmls

STUDENT_DATA_DIR = 'S:\\Reporting & Data\\Life Design Educator Engagement\\StudentData'
ROSTER_FILEPATHS = [
    f'{STUDENT_DATA_DIR}\\sis_undergrads_2019_09_20.csv',
    f'{STUDENT_DATA_DIR}\\sis_graduate_students_2019_10_02.csv',
]
HANDSHAKE_DATA_FILEPATH = f'{STUDENT_DATA_DIR}\\handshake_hwd_students_2019_10_08.csv'
MAJORS_FILEPATH = f'{STUDENT_DATA_DIR}\\all_majors.csv'
ATHLETE_FILEPATH = f'{STUDENT_DATA_DIR}\\student_athlete_roster_2019_09_19.csv'

if __name__ == '__main__':
    with BrowsingSession() as browser:
        clean_appt_data = run_office_hours_etl(browser)
        clean_event_data = run_events_etl(browser)
        clean_fair_data = run_career_fair_etl(browser)
        engagement_data = clean_appt_data + clean_event_data + clean_fair_data
        write_engagement_data(CONFIG['engagement_data_filepath'], engagement_data)

    student_data = run_data_file_etl(ROSTER_FILEPATHS, HANDSHAKE_DATA_FILEPATH, MAJORS_FILEPATH, ATHLETE_FILEPATH)
    roster_data = run_roster_file_etl(ROSTER_FILEPATHS, HANDSHAKE_DATA_FILEPATH, MAJORS_FILEPATH, ATHLETE_FILEPATH)
    write_to_csv(CONFIG['student_data_filepath'], student_data)
    write_roster_excel_file(CONFIG['student_roster_filepath'], roster_data)
