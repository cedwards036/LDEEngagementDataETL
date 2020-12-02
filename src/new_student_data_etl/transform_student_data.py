import numpy as np
import pandas as pd

from src.data_model import Departments


def clean_potentially_mistyped_bool_fields(students: pd.DataFrame) -> pd.DataFrame:
    string_bool_fields = ['is_first_generation', 'is_urm', 'is_ep']
    for field in string_bool_fields:
        students = clean_mistyped_bool_field(students, field)
    return students


def clean_mistyped_bool_field(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    if df[column_name].dtype == 'bool':
        return df
    elif df[column_name].dtype == 'object':
        lower_column = df[column_name].fillna('').str.lower()
        df[column_name] = lower_column.replace({'true': True, 'false': False, '': None})
    elif df[column_name].dtype == 'float64' or df[column_name].dtype == 'int64':
        df[column_name] = df[column_name].astype('object')
    return df


def merge_with_handshake_data(students: pd.DataFrame, handshake_data: pd.DataFrame) -> pd.DataFrame:
    return students.merge(handshake_data, how='left', on='jhed')


def melt_majors(students: pd.DataFrame) -> pd.DataFrame:
    split_majors = students['majors'].str.split(';', expand=True)
    split_major_columns = list(split_majors.columns)
    split_majors['hopkins_id'] = students['hopkins_id']
    melted_majors = split_majors.melt(id_vars=['hopkins_id'], value_vars=split_major_columns, value_name='major').dropna()
    melted_majors = melted_majors.drop(columns=['variable'])
    students = students.merge(melted_majors, how='left', on='hopkins_id')
    students = students.drop(columns=['majors'])
    return students


def clean_majors(students: pd.DataFrame) -> pd.DataFrame:
    def clean_major(major: str) -> str:
        lowercase_major = major.lower()
        if ':' in lowercase_major:
            if lowercase_major.startswith('m.') or lowercase_major.startswith('ph.d'):
                return major
            else:
                return major[major.index(':') + 1:].strip()
        else:
            return major

    students['major'] = students['major'].apply(clean_major)
    return students


def add_major_metadata(students: pd.DataFrame, major_metadata: pd.DataFrame) -> pd.DataFrame:
    merged_data = students.merge(major_metadata, how='left', on='major')
    merged_data = merged_data.rename(columns={'department': 'major_department'})
    merged_data.loc[merged_data['is_ep'], ['college', 'major_department']] = ['wse', Departments.EP.value.name]
    return merged_data


def add_athlete_data(students: pd.DataFrame, athlete_data: pd.DataFrame) -> pd.DataFrame:
    students = students.merge(athlete_data, how='left', left_on='hopkins_id', right_on='University ID')
    students = students.drop(columns=['University ID'])
    students = students.rename(columns={'Sport': 'sport'})
    students['is_athlete'] = ~students['sport'].isna()
    return students


def add_sli_data(students: pd.DataFrame, sli_data: pd.DataFrame) -> pd.DataFrame:
    students = students.merge(sli_data, how='left', on='hopkins_id')
    students['is_in_org'] = ~students['is_top_4_officer'].isna()
    students['is_top_4_officer'] = students['is_top_4_officer'].fillna(False)
    return students


def make_student_department_table(students: pd.DataFrame) -> pd.DataFrame:
    if students.empty:
        return pd.DataFrame(data={'hopkins_id': [], 'department': []})
    else:
        sub_tables = []
        for hopkins_id in students['hopkins_id'].unique():
            sub_tables.append(make_student_department_subtable(students, hopkins_id))
        return pd.concat(sub_tables, ignore_index=True)


def make_student_department_subtable(students: pd.DataFrame, hopkins_id: str) -> pd.DataFrame:
    def is_freshman(student_df: pd.DataFrame) -> bool:
        return student_df.iloc[0]['school_year'] == 'Freshman'

    def is_undergrad(student_df: pd.DataFrame) -> bool:
        return student_df.iloc[0]['school_year'] in ['Freshman', 'Sophomore', 'Junior', 'Senior']

    def is_ep(student_df: pd.DataFrame) -> bool:
        return student_df.iloc[0]['is_ep']

    def is_bme(student_df: pd.DataFrame) -> bool:
        return student_df.iloc[0]['major_department'] == Departments.BME.value.name

    def create_student_department_table() -> pd.DataFrame:
        return pd.DataFrame({'hopkins_id': [], 'department': []})

    def add_major_depts(student_df: pd.DataFrame, department_table: pd.DataFrame) -> pd.DataFrame:
        major_depts = student_df[['hopkins_id', 'major_department']]
        major_depts = major_depts.rename(columns={'major_department': 'department'})
        return pd.concat([major_depts, department_table])

    def add_ep_dept(department_table: pd.DataFrame) -> pd.DataFrame:
        return append_department(hopkins_id, Departments.EP.value.name, department_table)

    def add_soar_departments(student_df: pd.DataFrame, table_df: pd.DataFrame) -> pd.DataFrame:
        if student_df.iloc[0]['is_athlete'] == True:
            table_df = append_department(hopkins_id, Departments.SOAR_ATHLETICS.value.name, table_df)
        if is_undergrad(student_df):
            if is_freshman(student_df):
                if 'ksas' in student_df['college'].values:
                    table_df = append_department(hopkins_id, Departments.SOAR_FYE_KSAS.value.name, table_df)
                if 'wse' in student_df['college'].values:
                    table_df = append_department(hopkins_id, Departments.SOAR_FYE_WSE.value.name, table_df)
            if student_df.iloc[0]['is_in_org'] == True:
                table_df = append_department(hopkins_id, Departments.SOAR_SLI.value.name, table_df)
            if student_df.iloc[0]['is_urm'] == True or student_df.iloc[0]['is_first_generation'] == True or student_df.iloc[0]['is_pell_eligible'] == True:
                if student_df.iloc[0]['is_pre_med'] == True:
                    table_df = append_department(hopkins_id, Departments.SOAR_CSS.value.name, table_df)
                elif student_df.iloc[0]['is_athlete'] == False and student_df.iloc[0]['is_in_org'] == False and not is_freshman(student_df):
                    table_df = append_department(hopkins_id, Departments.SOAR_DIV_INCL.value.name, table_df)
        return table_df

    def append_department(hopkins_id: str, department: str, table: pd.DataFrame) -> pd.DataFrame:
        return table.append(pd.DataFrame(data={
            'hopkins_id': [hopkins_id],
            'department': [department]
        }), ignore_index=True)

    student_df = students.loc[students['hopkins_id'] == hopkins_id]
    student_dept_table = create_student_department_table()
    if not student_df.empty:
        if (not is_freshman(student_df)) or is_bme(student_df):
            student_dept_table = add_major_depts(student_df, student_dept_table)
        student_dept_table = add_soar_departments(student_df, student_dept_table)
    student_dept_table = student_dept_table.drop_duplicates().reset_index(drop=True)
    return student_dept_table


def merge_with_student_department_data(students: pd.DataFrame, student_department_data: pd.DataFrame) -> pd.DataFrame:
    return students.merge(student_department_data, how='left', on='hopkins_id')


def merge_with_engagement_data(students: pd.DataFrame, engagement_data: pd.DataFrame) -> pd.DataFrame:
    merged = students.merge(engagement_data, how='left', left_on='handshake_id', right_on='student_handshake_id')
    merged = merged.drop(columns=['student_handshake_id'])
    engagement_columns = engagement_data.iloc[:, 1:].columns
    merged[engagement_columns] = merged[engagement_columns].fillna(0).astype(np.int64)
    return merged
