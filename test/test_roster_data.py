import unittest

from src.roster_data import (transform_handshake_data, transform_roster_data,
                             enrich_with_handshake_data, enrich_with_dept_college_data)


class TestHandshakeData(unittest.TestCase):

    def test_transform_unique_handshake_data(self):
        test_data = [
            {
                'Students ID': '8029439',
                'Students Username': '49gj40',
                'Majors Name': 'B.S. Comp. Sci.: Computer Science',
                'School Year Name': 'Junior'
            },
            {
                'Students ID': '4325243',
                'Students Username': '82t349',
                'Majors Name': 'B.A.: English',
                'School Year Name': 'Senior'
            }
        ]

        expected = {
            '49gj40': {
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science'],
                'school_year': 'Junior'
            },
            '82t349': {
                'handshake_id': '4325243',
                'majors': ['B.A.: English'],
                'school_year': 'Senior'
            }
        }

        self.assertEqual(expected, transform_handshake_data(test_data))

    def test_transform_duplicate_handshake_data(self):
        test_data = [
            {
                'Students ID': '8029439',
                'Students Username': '49gj40',
                'Majors Name': 'B.S. Comp. Sci.: Computer Science',
                'School Year Name': 'Junior'
            },
            {
                'Students ID': '8029439',
                'Students Username': '49gj40',
                'Majors Name': 'B.S. AMS: Applied Math and Stats',
                'School Year Name': 'Junior'
            },
        ]

        expected = {
            '49gj40': {
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science', 'B.S. AMS: Applied Math and Stats'],
                'school_year': 'Junior'
            },
        }

        self.assertEqual(expected, transform_handshake_data(test_data))


class TestRosterData(unittest.TestCase):

    def test_transform_roster_data_single_majors(self):
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

    def test_enrich_with_handshake_data(self):
        test_data = [
            {
                'handshake_username': '49gj40'
            },
            {
                'handshake_username': '82t349'
            }
        ]

        test_hs_data = {
            '49gj40': {
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science', 'B.S. AMS: Applied Math and Stats'],
                'school_year': 'Junior'
            },
            '82t349': {
                'handshake_id': '4325243',
                'majors': ['B.A.: English'],
                'school_year': 'Senior'
            }
        }

        expected = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'B.S. Comp. Sci.: Computer Science',
                'school_year': 'Junior'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'B.S. AMS: Applied Math and Stats',
                'school_year': 'Junior'
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'major': 'B.A.: English',
                'school_year': 'Senior'
            }
        ]
        self.assertEqual(expected, enrich_with_handshake_data(test_data, test_hs_data))


class TestDeptCollegeEnrichment(unittest.TestCase):
    def test_enrich_with_dept_and_college_data(self):
        test_data = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'B.S. Comp. Sci.: Computer Science',
                'school_year': 'Junior'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'B.S. AMS: Applied Math and Stats',
                'school_year': 'Junior'
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'major': 'B.A.: English',
                'school_year': 'Sophomore'
            }
        ]

        test_dept_college_data = {
            'B.S. Comp. Sci.: Computer Science': {
                'department': 'comp_elec_eng',
                'college': 'wse'
            },
            'B.S. AMS: Applied Math and Stats': {
                'department': 'misc_eng',
                'college': 'wse'
            },
            'B.A.: English': {
                'department': 'lit_lang_film',
                'college': 'ksas'
            }
        }

        expected = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'B.S. Comp. Sci.: Computer Science',
                'school_year': 'Junior',
                'department': 'comp_elec_eng',
                'college': 'wse'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'B.S. AMS: Applied Math and Stats',
                'school_year': 'Junior',
                'department': 'misc_eng',
                'college': 'wse'
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'major': 'B.A.: English',
                'school_year': 'Sophomore',
                'department': 'lit_lang_film',
                'college': 'ksas'
            },
        ]
        self.assertEqual(expected, enrich_with_dept_college_data(test_data, test_dept_college_data))

    def test_enrich_freshman_data(self):
        test_data = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'Pre-Major',
                'school_year': 'Freshman'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'B.S. AMS: Applied Math and Stats',
                'school_year': 'Freshman'
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'major': 'B.A.: English',
                'school_year': 'Freshman'
            }
        ]

        test_dept_college_data = {
            'Pre-Major': {
                'department': 'soar_fye_ksas',
                'college': 'ksas'
            },
            'B.S. AMS: Applied Math and Stats': {
                'department': 'misc_eng',
                'college': 'wse'
            },
            'B.A.: English': {
                'department': 'lit_lang_film',
                'college': 'ksas'
            }
        }

        expected = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'Pre-Major',
                'school_year': 'Freshman',
                'department': 'soar_fye_ksas',
                'college': 'ksas'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'B.S. AMS: Applied Math and Stats',
                'school_year': 'Freshman',
                'department': 'misc_eng',
                'college': 'wse'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'B.S. AMS: Applied Math and Stats',
                'school_year': 'Freshman',
                'department': 'soar_fye_wse',
                'college': 'wse'
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'major': 'B.A.: English',
                'school_year': 'Freshman',
                'department': 'lit_lang_film',
                'college': 'ksas'
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'major': 'B.A.: English',
                'school_year': 'Freshman',
                'department': 'soar_fye_ksas',
                'college': 'ksas'
            },
        ]
        self.assertEqual(expected, enrich_with_dept_college_data(test_data, test_dept_college_data))
