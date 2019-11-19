import unittest

from src.student_data_etl.extractors import (transform_athlete_data, transform_major_data,
                                             transform_handshake_data, transform_roster_data)
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

    def test_transform_unique_handshake_data(self):
        test_data = [
            {
                'Students ID': '8029439',
                'Students Username': '49gj40',
                'Majors Name': 'B.S. Comp. Sci.: Computer Science',
                'School Year Name': 'Junior',
                'Students Email': 'astu2@jhu.edu',
                'Students First Name': 'Arthur',
                'Students Preferred Name': 'Art',
                'Students Last Name': 'Student',
                'Institution Labels Name List': ''
            },
            {
                'Students ID': '4325243',
                'Students Username': '82t349',
                'Majors Name': 'B.A.: English',
                'School Year Name': 'Senior',
                'Students Email': 'bstu2@jhu.edu',
                'Students First Name': 'Benjamin',
                'Students Preferred Name': '',
                'Students Last Name': 'Stuart',
                'Institution Labels Name List': ''
            }
        ]

        expected = {
            '49GJ40': {
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science'],
                'school_year': 'Junior',
                'email': 'astu2@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Student',
                'is_pre_med': False
            },
            '82T349': {
                'handshake_id': '4325243',
                'majors': ['B.A.: English'],
                'school_year': 'Senior',
                'email': 'bstu2@jhu.edu',
                'first_name': 'Benjamin',
                'pref_name': '',
                'last_name': 'Stuart',
                'is_pre_med': False
            }
        }

        self.assertEqual(expected, transform_handshake_data(test_data))

    def test_transform_duplicate_handshake_data(self):
        test_data = [
            {
                'Students ID': '8029439',
                'Students Username': '49gj40',
                'Majors Name': 'B.S. Comp. Sci.: Computer Science',
                'School Year Name': 'Junior',
                'Students Email': 'astu2@jhu.edu',
                'Students First Name': 'Arthur',
                'Students Preferred Name': 'Art',
                'Students Last Name': 'Student',
                'Institution Labels Name List': ''
            },
            {
                'Students ID': '8029439',
                'Students Username': '49gj40',
                'Majors Name': 'B.S. AMS: Applied Math and Stats',
                'School Year Name': 'Junior',
                'Students Email': 'astu2@jhu.edu',
                'Students First Name': 'Arthur',
                'Students Preferred Name': 'Art',
                'Students Last Name': 'Student',
                'Institution Labels Name List': ''
            },
        ]

        expected = {
            '49GJ40': {
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science', 'B.S. AMS: Applied Math and Stats'],
                'school_year': 'Junior',
                'email': 'astu2@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Student',
                'is_pre_med': False
            },
        }

        self.assertEqual(expected, transform_handshake_data(test_data))

    def test_transform_pre_med_handshake_data(self):
        test_data = [
            {
                'Students ID': '8029439',
                'Students Username': '49gj40',
                'Majors Name': 'B.S. Comp. Sci.: Computer Science',
                'School Year Name': 'Junior',
                'Students Email': 'astu2@jhu.edu',
                'Students First Name': 'Arthur',
                'Students Preferred Name': 'Art',
                'Students Last Name': 'Student',
                'Institution Labels Name List': 'system gen: hwd, hwd: pre-health, ferpa'
            }
        ]

        expected = {
            '49GJ40': {
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science'],
                'school_year': 'Junior',
                'email': 'astu2@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Student',
                'is_pre_med': True
            },
        }

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

    def test_transform_roster_data(self):
        test_roster_data = [
            {
                'FullName': 'Smith, John',
                'textbox7': '2f38987',
                'TypeSubType': 'ASEN - Ugrad/Bachelors',
                'Primary': 'Y',
                'Status': 'UG Current',
                'Alerts': 'N',
                'StartTerm': 'AE Fall 2018'
            },
            {
                'FullName': 'Johnson, Alice',
                'textbox7': '7987243',
                'TypeSubType': 'ASEN - Ugrad/Bachelors',
                'Primary': 'Y',
                'Status': 'UG Current',
                'Alerts': 'N',
                'StartTerm': 'AE Fall 2016'
            }
        ]

        expected = [
            {
                'handshake_username': '2f38987'
            },
            {
                'handshake_username': '7987243'
            }
        ]

        self.assertEqual(expected, transform_roster_data(test_roster_data))
