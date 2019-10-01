import unittest

from src.roster_data import (transform_handshake_data, transform_roster_data,
                             enrich_with_handshake_data, enrich_with_dept_college_data,
                             transform_major_data, transform_athlete_data,
                             enrich_with_athlete_data)


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
            '49GJ40': {
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science'],
                'school_year': 'Junior'
            },
            '82T349': {
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
            '49GJ40': {
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science', 'B.S. AMS: Applied Math and Stats'],
                'school_year': 'Junior'
            },
        }

        self.assertEqual(expected, transform_handshake_data(test_data))


class TestMajorData(unittest.TestCase):

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
            'English': {
                'department': 'literature',
                'college': 'ksas'
            },
            'Comp Sci': {
                'department': 'comp_sci',
                'college': 'wse'
            }
        }

        self.assertEqual(expected, transform_major_data(test_data))


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
            '49GJ40': {
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science', 'B.S. AMS: Applied Math and Stats'],
                'school_year': 'Junior'
            },
            '82T349': {
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


class TestAthleteData(unittest.TestCase):

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
            }
        ]

        expected = {
            'F94T7R': 'Water Polo',
            'GT29FJ': 'Soccer'
        }
        self.assertEqual(expected, transform_athlete_data(test_data))

    def test_enrich_student_data_with_athlete_status(self):
        test_data = [
            {
                'handshake_username': 'f94t7r',
                'handshake_id': '8029439',
                'major': 'B.S. Comp. Sci.: Computer Science',
                'school_year': 'Junior',
                'extraneous_field': 'something'
            },
            {
                'handshake_username': 'gt29fj',
                'handshake_id': '8029439',
                'school_year': 'Junior',
                'department': 'comp_elec_eng'
            },
            {
                'handshake_username': '203rf8',
                'handshake_id': '92839843',
                'school_year': 'Freshman',
                'department': 'humanities'
            },
        ]

        test_athlete_data = {
            'F94T7R': 'Water Polo',
            'GT29FJ': 'Soccer'
        }

        expected = [
            {
                'handshake_username': 'f94t7r',
                'handshake_id': '8029439',
                'major': 'B.S. Comp. Sci.: Computer Science',
                'school_year': 'Junior',
                'extraneous_field': 'something',
                'is_athlete': True,
                'athlete_sport': 'Water Polo',
                'department': 'soar_athletics'
            },
            {
                'handshake_username': 'f94t7r',
                'handshake_id': '8029439',
                'major': 'B.S. Comp. Sci.: Computer Science',
                'school_year': 'Junior',
                'extraneous_field': 'something',
                'is_athlete': True,
                'athlete_sport': 'Water Polo'
            },
            {
                'handshake_username': 'gt29fj',
                'handshake_id': '8029439',
                'school_year': 'Junior',
                'is_athlete': True,
                'athlete_sport': 'Soccer',
                'department': 'soar_athletics'
            },
            {
                'handshake_username': 'gt29fj',
                'handshake_id': '8029439',
                'school_year': 'Junior',
                'is_athlete': True,
                'athlete_sport': 'Soccer',
                'department': 'comp_elec_eng'
            },
            {
                'handshake_username': '203rf8',
                'handshake_id': '92839843',
                'school_year': 'Freshman',
                'is_athlete': False,
                'athlete_sport': None,
                'department': 'humanities'
            }
        ]
        self.assertEqual(expected, enrich_with_athlete_data(test_data, test_athlete_data))

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
