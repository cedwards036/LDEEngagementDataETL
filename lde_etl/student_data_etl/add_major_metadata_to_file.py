import pandas as pd

from lde_etl.student_data_etl.extract import get_handshake_data
from lde_etl.student_data_etl.extract import get_major_metadata
from lde_etl.student_data_etl.extract import get_athlete_data
from lde_etl.student_data_etl.transform_student_data import clean_potentially_mistyped_bool_fields
from lde_etl.student_data_etl.transform_student_data import add_major_metadata
from lde_etl.student_data_etl.transform_student_data import add_athlete_data
from lde_etl.student_data_etl.transform_student_data import clean_majors
from lde_etl.student_data_etl.transform_student_data import make_student_department_table
from lde_etl.student_data_etl.transform_student_data import melt_majors
from lde_etl.student_data_etl.transform_student_data import merge_with_handshake_data
from lde_etl.student_data_etl.transform_student_data import merge_with_student_department_data


def run_student_etl():
    print('Extracting student data...')
    students = clean_potentially_mistyped_bool_fields(pd.read_excel('C:\\Users\\cedwar42\\Downloads\\spring_2020.xlsx'))
    print('adding athlete data')
    athlete_data = get_athlete_data('C:\\Users\\cedwar42\\Downloads\\student_athlete_roster_2020_01_24.csv')
    students = add_athlete_data(students, athlete_data)
    print('Extracting major metadata...')
    major_metadata = get_major_metadata()

    print('Adding major and department data to student records...')
    students = melt_majors(students)
    students = clean_majors(students)
    students = add_major_metadata(students, major_metadata)
    student_departments = make_student_department_table(students)
    students = merge_with_student_department_data(students, student_departments)

    print('Extracting handshake data...')
    handshake_data = get_handshake_data()
    students = merge_with_handshake_data(students, handshake_data)

    print('Writing output to file...')
    students.to_excel('C:\\Users\\cedwar42\\Downloads\\student_data_from_file.xlsx', index=False)

    print('Done!')


if __name__ == '__main__':
    run_student_etl()
