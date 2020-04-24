import os

import pandas as pd

from src.common import BrowsingSession
from src.common import CONFIG
from src.common import read_csv
from src.file_writers import write_roster_excel_files
from src.new_student_data_etl.extract import STUDENTS_INSIGHTS_REPORT
from src.new_student_data_etl.sis_connection import SISConnection
from src.new_student_data_etl.transform_handshake_data import transform_handshake_data
from src.new_student_data_etl.transform_student_data import add_major_metadata
from src.new_student_data_etl.transform_student_data import make_student_department_table
from src.new_student_data_etl.transform_student_data import melt_majors
from src.new_student_data_etl.transform_student_data import clean_majors
from src.new_student_data_etl.transform_student_data import merge_with_handshake_data
from src.new_student_data_etl.transform_student_data import merge_with_student_department_data
from src.new_student_data_etl.transform_student_data import merge_with_engagement_data
from src.new_student_data_etl.transform_engagement_data import count_engagements_by_type

from src.new_student_data_etl.lde_roster_file import format_for_roster_file
from src.new_student_data_etl.lde_roster_file import split_into_separate_department_rosters


def read_file_to_string(file_path) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def get_sis_data() -> pd.DataFrame:
    sis_query_filepath = f'{os.path.dirname(os.path.abspath(__file__))}/sis_student_query.sql'
    with SISConnection() as cursor:
        return pd.DataFrame(cursor.select(read_file_to_string(sis_query_filepath)))


def get_major_metadata() -> pd.DataFrame:
    return pd.DataFrame(read_csv(f'{CONFIG["student_data_dir"]}\\major_metadata.csv'))


def get_handshake_data() -> pd.DataFrame:
    with BrowsingSession() as browser:
        return transform_handshake_data(pd.DataFrame(STUDENTS_INSIGHTS_REPORT.extract_data(browser)))


if __name__ == '__main__':
    print('Extracting SIS data...')
    students = get_sis_data()
    print('Extracting major metadata...')
    major_metadata = get_major_metadata()

    print('Adding major and department data to student records...')
    students = melt_majors(students)
    students = clean_majors(students)
    students = add_major_metadata(students, major_metadata)
    student_departments = make_student_department_table(students)
    student_departments.to_csv('C:\\Users\\cedwar42\\Downloads\\student_departments.csv', index=False)
    students = merge_with_student_department_data(students, student_departments)

    print('Extracting handshake data...')
    handshake_data = get_handshake_data()
    students = merge_with_handshake_data(students, handshake_data)

    print('Writing output to file...')
    students.to_csv('C:\\Users\\cedwar42\\Downloads\\student_data.csv', index=False)

    print('Creating roster file...')
    roster_file = format_for_roster_file(pd.read_csv('C:\\Users\\cedwar42\\Downloads\\student_data.csv'))
    engagement_data = count_engagements_by_type(pd.read_csv('S:\\Reporting & Data\\Life Design Educator Engagement\\engagement_data.csv', encoding='ISO-8859-1'))
    roster_file = merge_with_engagement_data(roster_file, engagement_data)
    department_roster_files = split_into_separate_department_rosters(roster_file)
    roster_dir = 'C:\\Users\\cedwar42\\Downloads\\lde_rosters\\'
    write_roster_excel_files(roster_dir, department_roster_files)

    print('Done!')

