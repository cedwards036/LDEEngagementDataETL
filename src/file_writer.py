import csv
from typing import List

from src.data_model import EngagementRecord


def write_engagement_data(filepath: str, office_hour_data):
    """Write engagement data to a csv file"""
    writeable_data = _make_engagement_data_writeable(office_hour_data)
    write_to_csv(filepath, writeable_data)


def write_to_csv(filepath: str, data: List[dict]):
    """Write data to a csv"""
    header = data[0].keys()
    with open(filepath, 'w') as file:
        dict_writer = csv.DictWriter(file, header, lineterminator='\n')
        dict_writer.writeheader()
        dict_writer.writerows(data)
    return filepath


def _make_engagement_data_writeable(engagement_data: List[EngagementRecord]) -> List[dict]:
    return [record.data for record in engagement_data]
