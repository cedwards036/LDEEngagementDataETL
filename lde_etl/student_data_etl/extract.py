import os
from datetime import datetime

import pandas as pd

from lde_etl.common import BrowsingSession
from lde_etl.common import InsightsReport
from lde_etl.common import read_csv
from lde_etl.data_model import EngagementRecord
from lde_etl.student_data_etl.sis_connection import SISConnection
from lde_etl.student_data_etl.transform_handshake_data import transform_handshake_data

STUDENTS_INSIGHTS_REPORT = InsightsReport(
    url='https://app.joinhandshake.com/analytics/reports/9241',
)


def read_file_to_string(file_path) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def get_student_sis_data() -> pd.DataFrame:
    return get_sis_data(f'{os.path.dirname(os.path.abspath(__file__))}/sis_student_query.sql')


def get_wse_masters_student_data() -> pd.DataFrame:
    return get_sis_data(f'{os.path.dirname(os.path.abspath(__file__))}/current_eng_masters_students.sql')


def get_wgs_sis_data() -> pd.DataFrame:
    return get_sis_data(f'{os.path.dirname(os.path.abspath(__file__))}/wgs_students.sql')


def get_sis_data(sis_query_filepath) -> pd.DataFrame:
    with SISConnection() as cursor:
        return pd.DataFrame(cursor.select(read_file_to_string(sis_query_filepath)))


def get_pell_data(filepath) -> pd.DataFrame:
    return pd.read_excel(filepath)


def get_major_metadata(filepath) -> pd.DataFrame:
    return pd.DataFrame(read_csv(filepath))


def get_athlete_data(filepath) -> pd.DataFrame:
    athlete_data = pd.read_csv(filepath)
    athlete_data = athlete_data[['University ID', 'Sport']]
    return athlete_data


def get_sli_data(filepath) -> pd.DataFrame:
    sli_data = pd.read_excel(filepath)
    sli_data = sli_data[['hopkins_id', 'is_top_4_officer']]
    return sli_data


def get_handshake_data(config) -> pd.DataFrame:
    with BrowsingSession(config) as browser:
        return transform_handshake_data(pd.DataFrame(STUDENTS_INSIGHTS_REPORT.extract_data(browser, config['download_dir'])))


def get_this_years_engagement_data(filepath) -> pd.DataFrame:
    engagement_data = pd.read_csv(filepath, encoding='ISO-8859-1')
    return engagement_data.loc[engagement_data['academic_year'] == EngagementRecord.academic_year(datetime.now())]
