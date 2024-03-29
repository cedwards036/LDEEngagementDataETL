import csv
from typing import List

import pandas as pd
from pandas import ExcelWriter

from lde_etl.data_model import EngagementRecord


def write_engagement_data(filepath: str, engagement_data: List[EngagementRecord]):
    """Write engagement data to a csv file"""
    writeable_data = [record.data for record in engagement_data]
    write_to_csv(filepath, writeable_data)


def write_to_csv(filepath: str, data: List[dict]):
    """Write data to a csv"""
    header = data[0].keys()
    with open(filepath, 'w') as file:
        dict_writer = csv.DictWriter(file, header, lineterminator='\n')
        dict_writer.writeheader()
        dict_writer.writerows(data)
    return filepath


def write_roster_excel_file(filepath: str, data: List[dict]):
    """Write student roster data to a multi-sheet excel file"""

    def _set_column_order(df: pd.DataFrame) -> pd.DataFrame:
        return df[['handshake_id', 'email', 'first_name', 'legal_first_name', 'pref_first_name', 'last_name',
                   'department', 'colleges', 'majors', 'school_year', 'is_pre_med',
                   'has_activated_handshake', 'has_completed_profile', 'is_athlete', 'sports']]

    def _adjust_column_widths(df: pd.DataFrame, worksheet):
        """Thanks to https://stackoverflow.com/a/40535454"""
        for idx, col in enumerate(df):  # loop through all columns
            series = df[col]
            max_len = max((
                series.astype(str).map(len).max(),  # len of largest item
                len(str(series.name))  # len of column name/header
            ))
            worksheet.set_column(idx, idx, max_len)  # set column width

    def _determine_sheet_name(department: str) -> str:
        if department == '':
            return 'no_department'
        else:
            return f'{department}_dept'

    def _write_department_roster_sheet(dept_roster: pd.DataFrame, sheet_name: str, writer: ExcelWriter):
        dept_roster.to_excel(writer, sheet_name=sheet_name, index=False)
        worksheet = writer.sheets[sheet_name]
        _adjust_column_widths(dept_roster, worksheet)

    df = pd.DataFrame(data)
    df = _set_column_order(df)

    departments = sorted(df['department'].unique())
    with ExcelWriter(filepath) as writer:
        for department in departments:
            dept_roster = df.loc[df['department'] == department]
            sheet_name = _determine_sheet_name(department)
            _write_department_roster_sheet(dept_roster, sheet_name, writer)
        writer.save()


def write_roster_excel_files(dir_path: str, rosters: List[pd.DataFrame]):

    def roster_file_name(roster: pd.DataFrame) -> str:
        return roster['department'][0] + '_roster'

    def _write_department_roster_sheet(roster: pd.DataFrame, writer: ExcelWriter):
        roster.to_excel(writer, index=False)
        worksheet = writer.sheets['Sheet1']
        _adjust_column_widths(roster, worksheet)

    def _adjust_column_widths(df: pd.DataFrame, worksheet):
        """Thanks to https://stackoverflow.com/a/40535454"""
        for idx, col in enumerate(df):  # loop through all columns
            series = df[col]
            max_len = max((
                series.astype(str).map(len).max(),  # len of largest item
                len(str(series.name))  # len of column name/header
            ))
            worksheet.set_column(idx, idx, max_len)  # set column width

    for roster in rosters:
        roster_filepath = dir_path + roster_file_name(roster) + '.xlsx'
        with ExcelWriter(roster_filepath) as writer:
            _write_department_roster_sheet(roster, writer)
            writer.save()
