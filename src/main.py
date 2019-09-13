from src.file_writer import write_engagement_data
from src.office_hours import extract_office_hours_data, transform_office_hours_data
from src.utils import BrowsingSession, CONFIG

if __name__ == '__main__':
    with BrowsingSession() as browser:
        raw_data = extract_office_hours_data(browser)
        clean_data = transform_office_hours_data(raw_data)
        write_engagement_data(CONFIG['engagement_data_filepath'], clean_data)
