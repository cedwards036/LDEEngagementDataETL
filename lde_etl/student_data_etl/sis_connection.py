import os
from typing import List

import pyodbc

from lde_etl.common import load_config

CONFIG_FILEPATH = f'{os.path.dirname(os.path.abspath(__file__))}/../../sis_config.json'
SIS_CONFIG = load_config(CONFIG_FILEPATH)


class SISConnection:

    def __enter__(self):
        self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + \
                                   SIS_CONFIG['server'] + ';DATABASE=' + \
                                   SIS_CONFIG['database'] + ';UID=' +
                                   ';Trusted_Connection=yes')
        self.cursor = self.cnxn.cursor()
        return SISCursor(self.cursor)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.cnxn.close()


class SISCursor:

    def __init__(self, cursor):
        self.cursor = cursor

    def select(self, sql: str) -> List[dict]:
        self.cursor.execute(sql)
        columns = [column[0] for column in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
