import csv
import json
import os
from datetime import datetime
from typing import List, Union

from autohandshake import HandshakeSession, HandshakeBrowser, InsightsPage, FileType

CONFIG_FILEPATH = f'{os.path.dirname(os.path.abspath(__file__))}/../config.json'


def load_config(config_filepath: str):
    """
    Load the configuration file
    :param config_filepath: the filepath to the config file
    :return: a dict of config values
    """
    with open(config_filepath, 'r') as file:
        return json.load(file)


CONFIG = load_config(CONFIG_FILEPATH)


class BrowsingSession(HandshakeSession):
    """
    A wrapper class around HandshakeSession that always logs into the same account.
    """

    def __init__(self, max_wait_time=300):
        super().__init__(CONFIG['handshake_url'], CONFIG['handshake_email'],
                         download_dir=CONFIG['download_dir'], chromedriver_path=CONFIG['chromedriver_path'], max_wait_time=max_wait_time)


class InsightsDateField:

    def set_report_date_range(self, insights_page: InsightsPage):
        pass


class RangeInsightsDateField(InsightsDateField):

    def __init__(self, date_field_category: str, date_field_title: str):
        self.date_field_category = date_field_category
        self.date_field_title = date_field_title

    def set_report_date_range(self, insights_page: InsightsPage):
        START_DATE = self._first_date_of_current_academic_year()
        END_DATE = datetime.today()
        insights_page.set_date_range_filter(field_category=self.date_field_category,
                                            field_title=self.date_field_title,
                                            start_date=START_DATE, end_date=END_DATE)
        return insights_page

    @staticmethod
    def _first_date_of_current_academic_year():
        JULY = 7
        if datetime.today().month < JULY:
            return datetime(datetime.today().year - 1, JULY, 1)
        else:
            return datetime(datetime.today().year, JULY, 1)


class NoInsightsDateField(InsightsDateField):

    def set_report_date_range(self, insights_page: InsightsPage):
        return insights_page


class InsightsReport:
    """
    A specification of an Inisghts report and its filterable date field.
    """

    def __init__(self, url: str, date_field: InsightsDateField = NoInsightsDateField()):
        self.url = url
        self._date_field = date_field

    def extract_data(self, browser: HandshakeBrowser) -> List[dict]:
        """
        Extract data from a Handshake insights page for the engagement report.

        :param browser: a logged-in HandshakeBrowser
        :param insights_url: a valid Insights report page url from which to get the data
        :return: the raw, extracted data in list-of-dict format
        """
        insights_page = InsightsPage(self.url, browser)
        insights_page = self._date_field.set_report_date_range(insights_page)
        downloaded_filepath = insights_page.download_file(CONFIG['download_dir'], file_type=FileType.JSON)
        return read_and_delete_json(downloaded_filepath)


def read_and_delete_json(filepath: str) -> List[dict]:
    """
    Read the given json file into a list of dicts, then delete the file

    :param filepath: the filepath of the json file to read
    :return: a list of dicts representing the json data
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    os.remove(filepath)
    return data


def read_csv(filepath: str) -> List[dict]:
    """
    Read the given csv file into a list of dicts

    :param filepath: the filepath of the csv file to read
    :return: a list of dicts representing the csv data
    """
    with open(filepath) as f:
        return [{k: v for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)]


def parse_date_string(date_str: str) -> datetime:
    """
    Parse a standard Handshake datetime string
    :param date_str:
    :return:
    """
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')


def convert_empty_str_to_none(value: str) -> Union[str, None]:
    if value == '':
        return None
    else:
        return value


def convert_none_to_empty_str(value: Union[str, None]) -> str:
    if value == None:
        return ''
    else:
        return value
