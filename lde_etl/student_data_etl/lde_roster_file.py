from typing import List

import numpy
import pandas as pd


def split_into_separate_department_rosters(roster: pd.DataFrame) -> List[pd.DataFrame]:
    roster['department'] = roster['department'].fillna('no_department')
    return [roster.loc[roster['department'] == department]
                .drop_duplicates()
                .reset_index(drop=True)
            for department in roster['department'].unique()]


def format_for_roster_file(students: pd.DataFrame) -> pd.DataFrame:
    students = unmelt_students_for_roster_file(students)
    students = filter_columns_for_roster_file(students)
    return students


def unmelt_students_for_roster_file(students: pd.DataFrame) -> pd.DataFrame:
    students = unmelt_and_join(students, 'major', 'majors')
    students = unmelt_and_join(students, 'college', 'colleges')
    students = unmelt_and_join(students, 'department', 'departments')
    students = students.drop(columns=['major', 'college'])
    students = students.drop_duplicates(['hopkins_id', 'department'])
    return students


def unmelt_and_join(students: pd.DataFrame, column_to_unmelt: str, unmelted_column_name: str) -> pd.DataFrame:
    def join_values(values: pd.Series) -> str:
        return ';'.join(numpy.sort(values.replace('', numpy.nan).dropna().unique()))

    unmelted_df = students.groupby('hopkins_id')[column_to_unmelt].apply(join_values).reset_index()
    unmelted_df = unmelted_df.rename(columns={column_to_unmelt: unmelted_column_name})
    students = students.merge(unmelted_df, on='hopkins_id', how='left')
    return students


def filter_columns_for_roster_file(students: pd.DataFrame) -> pd.DataFrame:
    return students[[
        'hopkins_id',
        'jhed',
        'email_address',
        'handshake_id',
        'first_name',
        'legal_first_name',
        'preferred_name',
        'last_name',
        'department',
        'departments',
        'colleges',
        'majors',
        'education_start_date',
        'school_year',
        'is_pre_med',
        'has_activated_handshake',
        'has_completed_profile',
        'is_athlete',
        'is_in_org',
        'is_top_4_officer',
        'gender',
        'is_first_generation',
        'is_pell_eligible',
        'is_urm',
        'citizenship',
    ]]
