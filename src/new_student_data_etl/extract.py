import os

import pandas as pd

from src.common import BrowsingSession
from src.common import CONFIG
from src.common import read_csv
from src.common import InsightsReport
from src.new_student_data_etl.sis_connection import SISConnection
from src.new_student_data_etl.transform_handshake_data import transform_handshake_data

STUDENTS_INSIGHTS_REPORT = InsightsReport(
    url='https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPWZnaHJkMzI4OHFtTHhUdEpJYjJmaFImZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9Zmls',
)

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