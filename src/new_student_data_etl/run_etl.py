import os
import pandas as pd

from src.new_student_data_etl.sis_connection import SISConnection
from src.new_student_data_etl.extract import STUDENTS_INSIGHTS_REPORT
from src.new_student_data_etl.transform_student_data import merge_with_handshake_data
from src.new_student_data_etl.transform_handshake_data import transform_handshake_data
from src.common import BrowsingSession

def read_file_to_string(file_path) -> str:
    with open(file_path, 'r') as file:
        return file.read()

def get_sis_data() -> pd.DataFrame:
    sis_query_filepath = f'{os.path.dirname(os.path.abspath(__file__))}/sis_student_query.sql'
    with SISConnection() as cursor:
        return pd.DataFrame(cursor.select(read_file_to_string(sis_query_filepath)))

def get_handshake_data() -> pd.DataFrame:
    with BrowsingSession() as browser:
        return transform_handshake_data(pd.DataFrame(STUDENTS_INSIGHTS_REPORT.extract_data(browser)))


if __name__ == '__main__':
    students = get_sis_data()
    handshake_data = get_handshake_data()
    students = merge_with_handshake_data(students, handshake_data)
    students.to_csv('C:\\Users\\cedwar42\\Downloads\\student_data.csv')
