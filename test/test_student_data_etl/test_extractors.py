import unittest
from datetime import datetime, timedelta

from src.handshake_fields import StudentFields
from src.student_data_etl.extractors import (transform_athlete_data, transform_major_data,
                                             transform_handshake_data, filter_handshake_data)
from src.student_data_etl.student_data_record import EducationRecord


class TestExtractorMiniTransformers(unittest.TestCase):

    def test_transform_major_data(self):
        test_data = [
            {
                'major': 'English',
                'department': 'literature',
                'college': 'ksas'
            },
            {
                'major': 'Comp Sci',
                'department': 'comp_sci',
                'college': 'wse'
            }
        ]

        expected = {
            'English': EducationRecord(
                major='English',
                department='literature',
                college='ksas'
            ),
            'Comp Sci': EducationRecord(
                major='Comp Sci',
                department='comp_sci',
                college='wse'
            )
        }

        self.assertEqual(expected, transform_major_data(test_data))

    def test_transform_major_data_with_missing_values(self):
        test_data = [
            {
                'major': 'English',
                'department': '',
                'college': ''
            },
        ]

        expected = {
            'English': EducationRecord(major='English'),
        }

        self.assertEqual(expected, transform_major_data(test_data))

    def test_filter_out_non_current_students(self):
        test_date = datetime(2020, 1, 23)
        good_labels = [f"temp: {(test_date - timedelta(days=i)).strftime('%Y-%m-%d')}" for i in range(4)]
        test_data = [
            {
                StudentFields.ID: '8029439',
                StudentFields.LABELS: good_labels[0]
            },
            {
                StudentFields.ID: '4325243',
                StudentFields.LABELS: good_labels[3]
            },
            {
                StudentFields.ID: '32674545',
                StudentFields.LABELS: good_labels[2]
            },
            {
                StudentFields.ID: '111646',
                StudentFields.LABELS: good_labels[1]
            },
            {
                StudentFields.ID: 'badstudent1',
                StudentFields.LABELS: 'temp: 2019-01-23'
            },
            {
                StudentFields.ID: 'badstudent2',
                StudentFields.LABELS: ''
            }
        ]

        expected = [
            {
                StudentFields.ID: '8029439',
                StudentFields.LABELS: good_labels[0]
            },
            {
                StudentFields.ID: '4325243',
                StudentFields.LABELS: good_labels[3]
            },
            {
                StudentFields.ID: '32674545',
                StudentFields.LABELS: good_labels[2]
            },
            {
                StudentFields.ID: '111646',
                StudentFields.LABELS: good_labels[1]
            }
        ]

        self.assertEqual(expected, filter_handshake_data(test_date, test_data))

    def test_filter_out_ep_students(self):
        test_date = datetime(2020, 1, 23)
        test_data = [
            {
                StudentFields.ID: '8029439',
                StudentFields.LABELS: f'temp: {test_date.strftime("%Y-%m-%d")}'
            },
            {
                StudentFields.ID: 'epstudent',
                StudentFields.LABELS: f'temp: {test_date.strftime("%Y-%m-%d")}, system gen: ep'
            }
        ]

        expected = [
            {
                StudentFields.ID: '8029439',
                StudentFields.LABELS: f'temp: {test_date.strftime("%Y-%m-%d")}'
            },
        ]

        self.assertEqual(expected, filter_handshake_data(test_date, test_data))

    def test_filter_out_hwd_location_labeled_students(self):
        test_date = datetime(2020, 1, 23)
        test_data = [
            {
                StudentFields.ID: '8029439',
                StudentFields.LABELS: f'temp: {test_date.strftime("%Y-%m-%d")}'
            },
            {
                StudentFields.ID: 'epstudent',
                StudentFields.LABELS: f'temp: {test_date.strftime("%Y-%m-%d")}, system gen: hwd location'
            }
        ]

        expected = [
            {
                StudentFields.ID: '8029439',
                StudentFields.LABELS: f'temp: {test_date.strftime("%Y-%m-%d")}'
            },
        ]

        self.assertEqual(expected, filter_handshake_data(test_date, test_data))

    def test_transform_unique_handshake_data(self):
        test_data = [
            {
                StudentFields.ID: '8029439',
                StudentFields.USERNAME: '49gj40',
                StudentFields.MAJOR: 'B.S. Comp. Sci.: Computer Science',
                StudentFields.SCHOOL_YEAR: 'Junior',
                StudentFields.EMAIL: 'astu2@jhu.edu',
                StudentFields.FIRST_NAME: 'Arthur',
                StudentFields.PREF_NAME: 'Art',
                StudentFields.LAST_NAME: 'Student',
                StudentFields.HAS_LOGGED_IN: 'Yes',
                StudentFields.HAS_COMPLETED_PROFILE: 'No',
                StudentFields.LABELS: ''
            },
            {
                StudentFields.ID: '4325243',
                StudentFields.USERNAME: '82t349',
                StudentFields.MAJOR: 'B.A.: English',
                StudentFields.SCHOOL_YEAR: 'Senior',
                StudentFields.EMAIL: 'bstu2@jhu.edu',
                StudentFields.FIRST_NAME: 'Benjamin',
                StudentFields.PREF_NAME: '',
                StudentFields.LAST_NAME: 'Stuart',
                StudentFields.HAS_LOGGED_IN: 'No',
                StudentFields.HAS_COMPLETED_PROFILE: 'No',
                StudentFields.LABELS: ''
            }
        ]

        expected = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science'],
                'school_year': 'Junior',
                'email': 'astu2@jhu.edu',
                'first_name': 'Art',
                'legal_first_name': 'Arthur',
                'pref_first_name': 'Art',
                'last_name': 'Student',
                'has_activated_handshake': True,
                'has_completed_profile': False,
                'is_pre_med': False
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'majors': ['B.A.: English'],
                'school_year': 'Senior',
                'email': 'bstu2@jhu.edu',
                'first_name': 'Benjamin',
                'legal_first_name': 'Benjamin',
                'pref_first_name': '',
                'last_name': 'Stuart',
                'has_activated_handshake': False,
                'has_completed_profile': False,
                'is_pre_med': False
            }
        ]

        self.assertEqual(expected, transform_handshake_data(test_data))

    def test_transform_duplicate_handshake_data(self):
        test_data = [
            {
                StudentFields.ID: '8029439',
                StudentFields.USERNAME: '49gj40',
                StudentFields.MAJOR: 'B.S. Comp. Sci.: Computer Science',
                StudentFields.SCHOOL_YEAR: 'Junior',
                StudentFields.EMAIL: 'astu2@jhu.edu',
                StudentFields.FIRST_NAME: 'Arthur',
                StudentFields.PREF_NAME: 'Art',
                StudentFields.LAST_NAME: 'Student',
                StudentFields.HAS_LOGGED_IN: 'Yes',
                StudentFields.HAS_COMPLETED_PROFILE: 'Yes',
                StudentFields.LABELS: ''
            },
            {
                StudentFields.ID: '8029439',
                StudentFields.USERNAME: '49gj40',
                StudentFields.MAJOR: 'B.S. AMS: Applied Math and Stats',
                StudentFields.SCHOOL_YEAR: 'Junior',
                StudentFields.EMAIL: 'astu2@jhu.edu',
                StudentFields.FIRST_NAME: 'Arthur',
                StudentFields.PREF_NAME: 'Art',
                StudentFields.LAST_NAME: 'Student',
                StudentFields.HAS_LOGGED_IN: 'Yes',
                StudentFields.HAS_COMPLETED_PROFILE: 'Yes',
                StudentFields.LABELS: ''
            },
        ]

        expected = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science', 'B.S. AMS: Applied Math and Stats'],
                'school_year': 'Junior',
                'email': 'astu2@jhu.edu',
                'first_name': 'Art',
                'legal_first_name': 'Arthur',
                'pref_first_name': 'Art',
                'last_name': 'Student',
                'has_activated_handshake': True,
                'has_completed_profile': True,
                'is_pre_med': False
            },
        ]

        self.assertEqual(expected, transform_handshake_data(test_data))

    def test_transform_pre_med_handshake_data(self):
        test_data = [
            {
                StudentFields.ID: '8029439',
                StudentFields.USERNAME: '49gj40',
                StudentFields.MAJOR: 'B.S. Comp. Sci.: Computer Science',
                StudentFields.SCHOOL_YEAR: 'Junior',
                StudentFields.EMAIL: 'astu2@jhu.edu',
                StudentFields.FIRST_NAME: 'Arthur',
                StudentFields.PREF_NAME: 'Art',
                StudentFields.LAST_NAME: 'Student',
                StudentFields.HAS_LOGGED_IN: 'Yes',
                StudentFields.HAS_COMPLETED_PROFILE: 'No',
                StudentFields.LABELS: 'system gen: hwd, hwd: pre-health, ferpa'
            }
        ]

        expected = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science'],
                'school_year': 'Junior',
                'email': 'astu2@jhu.edu',
                'first_name': 'Art',
                'legal_first_name': 'Arthur',
                'pref_first_name': 'Art',
                'last_name': 'Student',
                'has_activated_handshake': True,
                'has_completed_profile': False,
                'is_pre_med': True
            },
        ]

        self.assertEqual(expected, transform_handshake_data(test_data))

    def test_transform_athlete_data(self):
        test_data = [
            {
                'ID': '923809',
                'University ID': 'f94t7r',
                'First Name': 'John',
                'Last Name': 'Student',
                'Sport': 'Water Polo',
                'Grad. Year': '2022',
                'Email': 'jstudent@jhu.edu',
                'Mobile Phone': '9024098352',
                'Campus Address Street 1': '1 Street, Baltimore MD',
                'Birth Date': '1/1/2000'
            },
            {
                'ID': '4839589',
                'University ID': 'gt29fj',
                'First Name': 'Jane',
                'Last Name': 'Otherstudent',
                'Sport': 'Soccer',
                'Grad. Year': '2021',
                'Email': 'jotherstu@jhu.edu',
                'Mobile Phone': '8232938294',
                'Campus Address Street 1': '2 Ave, Baltimore MD',
                'Birth Date': '7/3/1999'
            },
            {
                'ID': '4839589',
                'University ID': 'gt29fj',
                'First Name': 'Jane',
                'Last Name': 'Otherstudent',
                'Sport': 'Tennis',
                'Grad. Year': '2021',
                'Email': 'jotherstu@jhu.edu',
                'Mobile Phone': '8232938294',
                'Campus Address Street 1': '2 Ave, Baltimore MD',
                'Birth Date': '7/3/1999'
            }
        ]

        expected = {
            'F94T7R': ['Water Polo'],
            'GT29FJ': ['Soccer', 'Tennis']
        }
        self.assertEqual(expected, transform_athlete_data(test_data))
