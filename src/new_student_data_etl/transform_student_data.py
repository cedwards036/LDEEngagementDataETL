import pandas as pd

from src.data_model import Departments


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


def add_major_metadata(students: pd.DataFrame, major_metadata: pd.DataFrame) -> pd.DataFrame:
    result = students.merge(major_metadata, how='left', on='major')
    result = result.rename(columns={'department': 'major_department'})
    return result


def make_student_department_table(students: pd.DataFrame) -> pd.DataFrame:
    if students.empty:
        return pd.DataFrame(data={'hopkins_id': [], 'department': []})
    else:
        sub_tables = []
        for hopkins_id in students['hopkins_id'].unique():
            sub_tables.append(make_student_department_subtable(students, hopkins_id))
        return pd.concat(sub_tables, ignore_index=True)


def make_student_department_subtable(students: pd.DataFrame, hopkins_id: str) -> pd.DataFrame:
    def create_student_dept_table_from_major_depts(df: pd.DataFrame) -> pd.DataFrame:
        student_dept_table = df[['hopkins_id', 'major_department']]
        return student_dept_table.rename(columns={'major_department': 'department'})

    def add_soar_departments(student_df: pd.DataFrame, table_df: pd.DataFrame) -> pd.DataFrame:
        if student_df.iloc[0]['school_year'] == 'Freshman':
            if 'ksas' in student_df['college'].values:
                table_df = append_department(Departments.SOAR_FYE_KSAS.value.name, table_df)
            if 'wse' in student_df['college'].values:
                table_df = append_department(Departments.SOAR_FYE_WSE.value.name, table_df)
        if student_df.iloc[0]['is_athlete']:
            table_df = append_department(Departments.SOAR_ATHLETICS.value.name, table_df)
        if student_df.iloc[0]['is_urm']:
            table_df = append_department(Departments.SOAR_DIV_INCL.value.name, table_df)
        return table_df

    def append_department(department: str, table: pd.DataFrame) -> pd.DataFrame:
        return table.append(pd.DataFrame(data={
            'hopkins_id': [hopkins_id],
            'department': [department]
        }), ignore_index=True)

    student_rows = students.loc[students['hopkins_id'] == hopkins_id]
    student_dept_table = create_student_dept_table_from_major_depts(student_rows)
    if not student_rows.empty:
        student_dept_table = add_soar_departments(student_rows, student_dept_table)
    student_dept_table = student_dept_table.drop_duplicates().reset_index(drop=True)
    return student_dept_table
