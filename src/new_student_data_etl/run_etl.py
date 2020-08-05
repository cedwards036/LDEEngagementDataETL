import pandas as pd

from src.file_writers import write_roster_excel_files
from src.new_student_data_etl.extract import get_handshake_data
from src.new_student_data_etl.extract import get_major_metadata
from src.new_student_data_etl.extract import get_sis_data
from src.new_student_data_etl.extract import get_athlete_data
from src.new_student_data_etl.lde_roster_file import format_for_roster_file
from src.new_student_data_etl.lde_roster_file import split_into_separate_department_rosters
from src.new_student_data_etl.transform_engagement_data import count_engagements_by_type
from src.new_student_data_etl.transform_student_data import clean_potentially_mistyped_bool_fields
from src.new_student_data_etl.transform_student_data import add_athlete_data
from src.new_student_data_etl.transform_student_data import add_major_metadata
from src.new_student_data_etl.transform_student_data import clean_majors
from src.new_student_data_etl.transform_student_data import make_student_department_table
from src.new_student_data_etl.transform_student_data import melt_majors
from src.new_student_data_etl.transform_student_data import merge_with_engagement_data
from src.new_student_data_etl.transform_student_data import merge_with_handshake_data
from src.new_student_data_etl.transform_student_data import merge_with_student_department_data


def run_student_etl():
    print('Extracting SIS data...')
    students = clean_potentially_mistyped_bool_fields(get_sis_data())

    print('Extracting athlete roster...')
    athlete_data = get_athlete_data('S:\\Reporting & Data\\Life Design Educator Engagement\\StudentData\\student_athlete_roster_2020_06_09.csv')
    students = add_athlete_data(students, athlete_data)

    print('Extracting handshake data...')
    handshake_data = get_handshake_data()
    students = merge_with_handshake_data(students, handshake_data)

    print('Extracting major metadata...')
    major_metadata = get_major_metadata()

    print('Adding major and department data to student records...')
    students = melt_majors(students)
    students = clean_majors(students)
    students = add_major_metadata(students, major_metadata)
    student_departments = make_student_department_table(students)
    student_departments.to_csv('C:\\Users\\cedwar42\\Downloads\\student_departments.csv', index=False)
    students = merge_with_student_department_data(students, student_departments)

    print('Writing output to file...')
    students.to_excel('C:\\Users\\cedwar42\\Downloads\\student_data.xlsx', index=False)

    print('Creating roster file...')
    roster_file = format_for_roster_file(pd.read_excel('C:\\Users\\cedwar42\\Downloads\\student_data.xlsx'))
    engagement_data = count_engagements_by_type(pd.read_csv('S:\\Reporting & Data\\Life Design Educator Engagement\\engagement_data.csv', encoding='ISO-8859-1'))
    roster_file = merge_with_engagement_data(roster_file, engagement_data)
    department_roster_files = split_into_separate_department_rosters(roster_file)
    roster_dir = 'C:\\Users\\cedwar42\\Downloads\\lde_rosters\\'
    write_roster_excel_files(roster_dir, department_roster_files)

    print('Done!')


if __name__ == '__main__':
    run_student_etl()
