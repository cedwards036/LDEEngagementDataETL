import pandas as pd
import glob

from lde_etl.file_writers import write_roster_excel_files
import lde_etl.student_data_etl.extract as extract
from lde_etl.student_data_etl.lde_roster_file import format_for_roster_file, split_into_separate_department_rosters
from lde_etl.student_data_etl.transform_engagement_data import count_engagements_by_type
import lde_etl.student_data_etl.transform_student_data as ts


def run_student_etl(config):
    print('Extracting SIS data...')
    students = ts.clean_potentially_mistyped_bool_fields(extract.get_student_sis_data())
    students = students.merge(extract.get_pell_data(config['pell_data_filepath']), how='left', on='hopkins_id')
    wgs_students = extract.get_wgs_sis_data()
    students = ts.add_wgs_data(students, wgs_students)
    wse_masters_students = extract.get_wse_masters_student_data()

    print('Extracting athlete roster...')
    athlete_data = extract.get_athlete_data(config['athlete_filepath'])
    students = ts.add_athlete_data(students, athlete_data)

    print('Extracting SLI roster...')
    sli_data = extract.get_sli_data(config['sli_filepath'])
    students = ts.add_sli_data(students, sli_data)

    print('Extracting handshake data...')
    handshake_data = extract.get_handshake_data(config)
    students = ts.merge_with_handshake_data(students, handshake_data)
    wse_masters_students = ts.merge_with_handshake_data(wse_masters_students, handshake_data)

    print('Extracting major metadata...')
    major_metadata = extract.get_major_metadata(config["major_metadata_filepath"])

    print('Adding major and department data to student records...')
    students = ts.melt_majors(students)
    students = ts.clean_majors(students)
    students = ts.add_major_metadata(students, major_metadata)
    student_departments = ts.make_student_department_table(students)
    student_departments.to_csv(config['student_departments_filepath'], index=False)
    students = ts.merge_with_student_department_data(students, student_departments)

    print('Writing output to file...')
    students.to_excel(config['current_semester_data_filepath'], index=False)
    wse_masters_students.to_excel(config['wse_masters_students_filepath'], index=False)

    print('Combining student data files...')
    combined = pd.concat([pd.read_excel(filename) for filename in glob.glob(config['semester_data_dir'] + "\\*.xlsx")], sort=True)
    combined.to_excel(config['student_data_filepath'], index=False)

    print('Creating roster file...')
    roster_file = format_for_roster_file(pd.read_excel(config['current_semester_data_filepath']))
    engagement_data = count_engagements_by_type(extract.get_this_years_engagement_data(config['engagement_data_filepath']))
    roster_file = ts.merge_with_engagement_data(roster_file, engagement_data)
    department_roster_files = split_into_separate_department_rosters(roster_file)
    for dir in config['lde_roster_dirs']:
        write_roster_excel_files(dir, department_roster_files)

    print('Done!')
