from src.office_hours import extract_office_hours_data
from src.utils import BrowsingSession

if __name__ == '__main__':
    with BrowsingSession() as browser:
        print(extract_office_hours_data(browser))
