import json
import os
from datetime import datetime
from typing import List

from autohandshake import HandshakeSession, HandshakeBrowser, InsightsPage, FileType

CONFIG_FILEPATH = '../config.json'


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
                         download_dir=CONFIG['download_dir'], max_wait_time=max_wait_time)


class InsightsReport:
    """
    A specification of an Inisghts report and its filterable date field.
    """

    def __init__(self, url: str, date_field_category: str, date_field_title):
        self.url = url
        self.date_field_category = date_field_category
        self.date_field_title = date_field_title

    def extract_data(self, browser: HandshakeBrowser) -> List[dict]:
        """
        Extract data from a Handshake insights page for the engagement report.

        :param browser: a logged-in HandshakeBrowser
        :param insights_url: a valid Insights report page url from which to get the data
        :return: the raw, extracted data in list-of-dict format
        """
        insights_page = InsightsPage(self.url, browser)
        insights_page = self._set_report_date_range(insights_page)
        downloaded_filepath = insights_page.download_file(CONFIG['download_dir'], file_type=FileType.JSON)
        return read_and_delete_json(downloaded_filepath)

    def _set_report_date_range(self, insights_page: InsightsPage):
        START_DATE = datetime(2019, 7, 1)
        END_DATE = datetime.today()
        insights_page.set_date_range_filter(field_category=self.date_field_category,
                                            field_title=self.date_field_title,
                                            start_date=START_DATE, end_date=END_DATE)
        return insights_page


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


def parse_date_string(date_str: str) -> datetime:
    """
    Parse a standard Handshake datetime string
    :param date_str:
    :return:
    """
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
