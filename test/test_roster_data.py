import unittest

from src.roster_data import (transform_handshake_data, transform_roster_data,
                             enrich_with_dept_college_data_for_data_file,
                             filter_handshake_data_with_sis_roster,
                             transform_major_data, transform_athlete_data,
                             enrich_with_athlete_data, filter_dict)


class TestHandshakeData(unittest.TestCase):

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
                'Students Last Name': 'Student'
            },
            {
                'Students ID': '4325243',
                'Students Username': '82t349',
                'Majors Name': 'B.A.: English',
                'School Year Name': 'Senior',
                'Students Email': 'bstu2@jhu.edu',
                'Students First Name': 'Benjamin',
                'Students Preferred Name': '',
                'Students Last Name': 'Stuart'
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
                'last_name': 'Student'
            },
            '82T349': {
                'handshake_id': '4325243',
                'majors': ['B.A.: English'],
                'school_year': 'Senior',
                'email': 'bstu2@jhu.edu',
                'first_name': 'Benjamin',
                'pref_name': '',
                'last_name': 'Stuart'
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
                'Students Last Name': 'Student'
            },
            {
                'Students ID': '8029439',
                'Students Username': '49gj40',
                'Majors Name': 'B.S. AMS: Applied Math and Stats',
                'School Year Name': 'Junior',
                'Students Email': 'astu2@jhu.edu',
                'Students First Name': 'Arthur',
                'Students Preferred Name': 'Art',
                'Students Last Name': 'Student'
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
                'last_name': 'Student'
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

    def test_filter_handshake_data_with_sis_roster(self):
        test_hs_data = {
            '49GJ40': {
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science', 'B.S. AMS: Applied Math and Stats'],
                'school_year': 'Junior',
                'email': 'astu2@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Student'
            },
            '82T349': {
                'handshake_id': '4325243',
                'majors': ['B.A.: English'],
                'school_year': 'Senior',
                'email': 'astu3@jhu.edu',
                'first_name': 'Alice',
                'pref_name': '',
                'last_name': 'Stuewcz'
            },
            'JT45UY': {
                'handshake_id': '9483059',
                'majors': ['B.A.: Int. Studies'],
                'school_year': 'Sophomore',
                'email': 'bcol43@jhu.edu',
                'first_name': 'Barnabus',
                'pref_name': '',
                'last_name': 'Charleston'
            }
        }

        test_sis_data = [
            {
                'handshake_username': '49gj40'
            },
            {
                'handshake_username': '82t349'
            }
        ]

        expected = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science', 'B.S. AMS: Applied Math and Stats'],
                'school_year': 'Junior',
                'email': 'astu2@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Student'
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'majors': ['B.A.: English'],
                'school_year': 'Senior',
                'email': 'astu3@jhu.edu',
                'first_name': 'Alice',
                'pref_name': '',
                'last_name': 'Stuewcz'
            },
        ]

        self.assertEqual(expected, filter_handshake_data_with_sis_roster(test_hs_data, test_sis_data))

    def test_filter_handshake_data_with_sis_roster_throws_error_when_student_not_found(self):
        test_hs_data = {
            '49GJ40': {},
            '82T349': {},
            'JT45UY': {}
        }

        test_sis_data = [
            {
                'handshake_username': '49GJ40'
            },
            {
                'handshake_username': '325245'
            }
        ]

        with self.assertRaises(ValueError):
            filter_handshake_data_with_sis_roster(test_hs_data, test_sis_data)


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
    def test_enrich_with_dept_and_college_data_for_data_file(self):
        test_data = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science', 'B.S. AMS: Applied Math and Stats'],
                'school_year': 'Junior',
                'email': 'astu2@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Student'
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'majors': ['B.A.: English'],
                'school_year': 'Senior',
                'email': 'astu3@jhu.edu',
                'first_name': 'Alice',
                'pref_name': '',
                'last_name': 'Stuewcz'
            },
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
                'major': 'Computer Science',
                'school_year': 'Junior',
                'department': 'comp_elec_eng',
                'college': 'wse',
                'email': 'astu2@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Student'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'Applied Math and Stats',
                'school_year': 'Junior',
                'department': 'misc_eng',
                'college': 'wse',
                'email': 'astu2@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Student'
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'major': 'English',
                'school_year': 'Senior',
                'department': 'lit_lang_film',
                'college': 'ksas',
                'email': 'astu3@jhu.edu',
                'first_name': 'Alice',
                'pref_name': '',
                'last_name': 'Stuewcz'
            },
        ]
        self.assertEqual(expected, enrich_with_dept_college_data_for_data_file(test_data, test_dept_college_data))

    def test_enrich_freshman_data(self):
        test_data = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'majors': ['Pre-Major', 'B.S. AMS: Applied Math and Stats'],
                'school_year': 'Freshman'
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'majors': ['B.A.: English'],
                'school_year': 'Freshman'
            },
            {
                'handshake_username': '2398ru3',
                'handshake_id': '93938028',
                'majors': ['M.S.: Computer Science'],
                'school_year': 'Masters'
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
            },
            'M.S.: Computer Science': {
                'department': 'eng_masters',
                'college': 'wse'
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
                'major': 'Applied Math and Stats',
                'school_year': 'Freshman',
                'department': 'misc_eng',
                'college': 'wse'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'Applied Math and Stats',
                'school_year': 'Freshman',
                'department': 'soar_fye_wse',
                'college': 'wse'
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'major': 'English',
                'school_year': 'Freshman',
                'department': 'lit_lang_film',
                'college': 'ksas'
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'major': 'English',
                'school_year': 'Freshman',
                'department': 'soar_fye_ksas',
                'college': 'ksas'
            },
            {
                'handshake_username': '2398ru3',
                'handshake_id': '93938028',
                'major': 'M.S.: Computer Science',
                'department': 'eng_masters',
                'college': 'wse',
                'school_year': 'Masters'
            }
        ]
        self.assertEqual(expected, enrich_with_dept_college_data_for_data_file(test_data, test_dept_college_data))

    def test_enrich_und_eng_freshman_data(self):
        test_data = [
            {
                'handshake_username': '8498j3g',
                'handshake_id': '173978344',
                'majors': ['Und Eng'],
                'school_year': 'Freshman'
            },
            {
                'handshake_username': '3538493',
                'handshake_id': '23920843',
                'majors': ['Bachelors: Und Eng'],
                'school_year': 'Freshman'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'majors': ['B.S. AMS: Applied Math and Stats'],
                'school_year': 'Freshman'
            }
        ]

        test_dept_college_data = {
            'Und Eng': {
                'department': 'soar_fye_wse',
                'college': 'wse'
            },
            'Bachelors: Und Eng': {
                'department': 'soar_fye_wse',
                'college': 'wse'
            },
            'B.S. AMS: Applied Math and Stats': {
                'department': 'misc_eng',
                'college': 'wse'
            }
        }

        expected = [
            {
                'handshake_username': '8498j3g',
                'handshake_id': '173978344',
                'major': 'Und Eng',
                'school_year': 'Freshman',
                'department': 'soar_fye_wse',
                'college': 'wse'
            },
            {
                'handshake_username': '3538493',
                'handshake_id': '23920843',
                'major': 'Und Eng',
                'school_year': 'Freshman',
                'department': 'soar_fye_wse',
                'college': 'wse'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'Applied Math and Stats',
                'school_year': 'Freshman',
                'department': 'misc_eng',
                'college': 'wse'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'major': 'Applied Math and Stats',
                'school_year': 'Freshman',
                'department': 'soar_fye_wse',
                'college': 'wse'
            }
        ]
        self.assertEqual(expected, enrich_with_dept_college_data_for_data_file(test_data, test_dept_college_data))


class TestFilterDict(unittest.TestCase):

    def test_filter_dict(self):
        test_dict = {
            'field_a': 1,
            'field_b': 2,
            'field_c': 3,
            'field_d': 4,
            'field_e': 5
        }
        allowed_fields = ['field_d', 'field_a']
        expected = {
            'field_a': 1,
            'field_d': 4,
        }
        self.assertEqual(expected, filter_dict(test_dict, allowed_fields))
