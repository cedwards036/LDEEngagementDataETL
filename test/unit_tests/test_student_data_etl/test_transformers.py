import unittest

from src.student_data_etl.student_data_record import EducationRecord, StudentRecord
from src.student_data_etl.transformers import (enrich_with_athlete_status,
                                               enrich_with_education_records,
                                               get_education_records_for_student)


def assert_lists_of_student_records_are_equal(test_class, expected, actual):
    def _to_dict(record: StudentRecord):
        result = record.to_dict()
        result['education_records'] = [ed_record.to_dict() for ed_record in result['education_records']]
        return result

    expected_lod = [_to_dict(record) for record in expected]
    actual_lod = [_to_dict(record) for record in actual]
    test_class.assertEqual(expected_lod, actual_lod)


class TestAthleteStatusEnrichment(unittest.TestCase):

    def test_enrich_student_data_with_athlete_status(self):
        test_data = [
            StudentRecord(
                handshake_username='f94t7r',
                handshake_id='8029439',
                school_year='Junior',
                education_data=[
                    EducationRecord(major='Computer Science', department='comp_elec_eng', college='wse')
                ]
            ),
            StudentRecord(
                handshake_username='gt29fj',
                handshake_id='3288234',
                school_year='Sophomore',
                education_data=[
                    EducationRecord(major='English', department='lit_lang_film', college='ksas')
                ]
            ),
            StudentRecord(
                handshake_username='203rf8',
                handshake_id='92839843',
                school_year='Freshman',
                education_data=[
                    EducationRecord(major='History', department='hist_phil_hum', college='ksas')
                ]
            )
        ]

        test_athlete_data = {
            'F94T7R': ['Water Polo'],
            'GT29FJ': ['Soccer', 'Tennis']
        }

        expected = [
            StudentRecord(
                handshake_username='f94t7r',
                handshake_id='8029439',
                school_year='Junior',
                education_data=[
                    EducationRecord(major='Computer Science', department='comp_elec_eng', college='wse')
                ],
                sports=['Water Polo']
            ),
            StudentRecord(
                handshake_username='gt29fj',
                handshake_id='3288234',
                school_year='Sophomore',
                education_data=[
                    EducationRecord(major='English', department='lit_lang_film', college='ksas')
                ],
                sports=['Soccer', 'Tennis']
            ),
            StudentRecord(
                handshake_username='203rf8',
                handshake_id='92839843',
                school_year='Freshman',
                education_data=[
                    EducationRecord(major='History', department='hist_phil_hum', college='ksas')
                ]
            )
        ]
        assert_lists_of_student_records_are_equal(self, expected,
                                                  enrich_with_athlete_status(test_data, test_athlete_data))


class TestDeptCollegeEnrichment(unittest.TestCase):

    def test_enrich_with_dept_and_college_data(self):
        test_data = [
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
                'is_pre_med': True,
                'has_activated_handshake': True,
                'has_completed_profile': True
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'majors': ['B.A.: English'],
                'school_year': 'Senior',
                'email': 'astu3@jhu.edu',
                'first_name': 'Alice',
                'legal_first_name': 'Alice',
                'pref_first_name': '',
                'last_name': 'Stuewcz',
                'is_pre_med': False,
                'has_activated_handshake': False,
                'has_completed_profile': False
            },
        ]

        test_dept_college_data = {
            'B.S. Comp. Sci.: Computer Science': EducationRecord(
                major='B.S. Comp. Sci.: Computer Science',
                department='comp_elec_eng',
                college='wse'
            ),
            'B.S. AMS: Applied Math and Stats': EducationRecord(
                major='B.S. AMS: Applied Math and Stats',
                department='misc_eng',
                college='wse'
            ),
            'B.A.: English': EducationRecord(
                major='B.A.: English',
                department='lit_lang_film',
                college='ksas'
            )
        }

        expected = [
            StudentRecord(
                handshake_username='49gj40',
                handshake_id='8029439',
                email='astu2@jhu.edu',
                first_name='Art',
                legal_first_name='Arthur',
                pref_first_name='Art',
                last_name='Student',
                school_year='Junior',
                is_pre_med=True,
                has_activated_handshake=True,
                has_completed_profile=True,
                education_data=[
                    EducationRecord(major='Computer Science', department='comp_elec_eng', college='wse'),
                    EducationRecord(major='Applied Math and Stats', department='misc_eng', college='wse')
                ]
            ),
            StudentRecord(
                handshake_username='82t349',
                handshake_id='4325243',
                email='astu3@jhu.edu',
                first_name='Alice',
                legal_first_name='Alice',
                last_name='Stuewcz',
                school_year='Senior',
                is_pre_med=False,
                has_activated_handshake=False,
                has_completed_profile=False,
                education_data=[
                    EducationRecord(major='English', department='lit_lang_film', college='ksas')
                ]
            )
        ]
        assert_lists_of_student_records_are_equal(self, expected,
                                                  enrich_with_education_records(test_data, test_dept_college_data))

    def test_enrich_freshman_with_defined_majors_with_dept_and_college_data(self):
        test_data = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '8029439',
                'majors': ['B.S. Comp. Sci.: Computer Science', 'B.S. AMS: Applied Math and Stats'],
                'school_year': 'Freshman',
                'email': 'astu2@jhu.edu',
                'first_name': 'Art',
                'legal_first_name': 'Arthur',
                'pref_first_name': 'Art',
                'last_name': 'Student',
                'is_pre_med': False,
                'has_activated_handshake': False,
                'has_completed_profile': False
            },
            {
                'handshake_username': '82t349',
                'handshake_id': '4325243',
                'majors': ['B.A.: English', 'B.S. Comp. Sci.: Computer Science'],
                'school_year': 'Freshman',
                'email': 'astu3@jhu.edu',
                'first_name': 'Alice',
                'legal_first_name': 'Alice',
                'pref_first_name': '',
                'last_name': 'Stuewcz',
                'is_pre_med': True,
                'has_activated_handshake': False,
                'has_completed_profile': False
            },
        ]

        test_dept_college_data = {
            'B.S. Comp. Sci.: Computer Science': EducationRecord(
                major='B.S. Comp. Sci.: Computer Science',
                department='comp_elec_eng',
                college='wse'
            ),
            'B.S. AMS: Applied Math and Stats': EducationRecord(
                major='B.S. AMS: Applied Math and Stats',
                department='misc_eng',
                college='wse'
            ),
            'B.A.: English': EducationRecord(
                major='B.A.: English',
                department='lit_lang_film',
                college='ksas'
            )
        }

        expected = [
            StudentRecord(
                handshake_username='49gj40',
                handshake_id='8029439',
                email='astu2@jhu.edu',
                first_name='Art',
                legal_first_name='Arthur',
                pref_first_name='Art',
                last_name='Student',
                school_year='Freshman',
                is_pre_med=False,
                has_activated_handshake=False,
                has_completed_profile=False,
                education_data=[
                    EducationRecord(major='Computer Science', department='comp_elec_eng', college='wse'),
                    EducationRecord(major='Applied Math and Stats', department='misc_eng', college='wse')
                ],
                additional_departments=['soar_fye_wse']
            ),
            StudentRecord(
                handshake_username='82t349',
                handshake_id='4325243',
                email='astu3@jhu.edu',
                first_name='Alice',
                legal_first_name='Alice',
                last_name='Stuewcz',
                school_year='Freshman',
                is_pre_med=True,
                has_activated_handshake=False,
                has_completed_profile=False,
                education_data=[
                    EducationRecord(major='English', department='lit_lang_film', college='ksas'),
                    EducationRecord(major='Computer Science', department='comp_elec_eng', college='wse')
                ],
                additional_departments=['soar_fye_wse', 'soar_fye_ksas']
            )
        ]
        assert_lists_of_student_records_are_equal(self, expected, enrich_with_education_records(test_data, test_dept_college_data))


class TestGetEducationRecordsForStudent(unittest.TestCase):

    def test_with_no_major(self):
        test_student_data = [
            {
                'majors': [],
                'school_year': 'Sophomore',
            },
            {
                'majors': [''],
                'school_year': 'Senior',
            },
        ]
        test_dept_college_data = {}
        expected = [EducationRecord()]
        for row in test_student_data:
            self.assertEqual(expected, get_education_records_for_student(row, test_dept_college_data))

    def test_interdisciplinary_major(self):
        test_student_data = {
            'majors': ['Interdisciplinary Studies'],
            'school_year': 'Junior',
        }
        test_dept_college_data = {}
        expected = [EducationRecord(major='Interdisciplinary Studies')]
        self.assertEqual(expected, get_education_records_for_student(test_student_data, test_dept_college_data))

    def test_interdisciplinary_major_alongside_other_majors(self):
        test_student_data = {
            'majors': ['B.S.: Interdisciplinary Studies', 'Math'],
            'school_year': 'Junior',
        }
        test_dept_college_data = {
            'Math': EducationRecord(
                major='Math',
                department='phys_env_sci',
                college='ksas'
            )
        }
        expected = [EducationRecord(major='Interdisciplinary Studies'),
                    EducationRecord(major='Math', department='phys_env_sci', college='ksas')]
        self.assertEqual(expected, get_education_records_for_student(test_student_data, test_dept_college_data))

    def test_no_match_throws_exception(self):
        test_student_data = {
            'majors': ['Some Unknown Major'],
            'school_year': 'Sophomore',
        }

        test_dept_college_data = {
            'B.S. Comp. Sci.: Computer Science': EducationRecord(
                major='B.S. Comp. Sci.: Computer Science',
                department='comp_elec_eng',
                college='wse'
            )
        }
        with self.assertRaises(ValueError):
            get_education_records_for_student(test_student_data, test_dept_college_data)

    def test_with_one_major(self):
        test_student_data = {
            'majors': ['B.S.: Comp. Sci.'],
            'school_year': 'Sophomore',
        }

        test_dept_college_data = {
            'B.S.: Comp. Sci.': EducationRecord(
                major='B.S.: Comp. Sci.',
                department='comp_elec_eng',
                college='wse'
            )
        }
        expected = [EducationRecord(
            major='Comp. Sci.',
            department='comp_elec_eng',
            college='wse'
        )]
        self.assertEqual(expected, get_education_records_for_student(test_student_data, test_dept_college_data))

    def test_with_multiple_majors(self):
        test_student_data = {
            'majors': ['B.S.: Comp. Sci.', 'M.S.E.: Mech Eng', 'Art History'],
            'school_year': 'Sophomore',
        }

        test_dept_college_data = {
            'B.S.: Comp. Sci.': EducationRecord(
                major='B.S.: Comp. Sci.',
                department='comp_elec_eng',
                college='wse'
            ),
            'M.S.E.: Mech Eng': EducationRecord(
                major='M.S.E.: Mech Eng',
                department='eng_masters',
                college='wse'
            ),
            'Art History': EducationRecord(
                major='Art History',
                department='hist_phil_hum',
                college='ksas'
            )
        }

        expected = [EducationRecord(major='Comp. Sci.', department='comp_elec_eng', college='wse'),
                    EducationRecord(major='M.S.E.: Mech Eng', department='eng_masters', college='wse'),
                    EducationRecord(major='Art History', department='hist_phil_hum', college='ksas')]
        self.assertEqual(expected, get_education_records_for_student(test_student_data, test_dept_college_data))

    def test_wse_freshman_with_defined_major(self):
        test_student_data = {
            'majors': ['B.S.: Comp. Sci.'],
            'school_year': 'Freshman',
        }

        test_dept_college_data = {
            'B.S.: Comp. Sci.': EducationRecord(
                major='B.S.: Comp. Sci.',
                department='comp_elec_eng',
                college='wse'
            )
        }
        expected = [EducationRecord(major='Comp. Sci.', department='comp_elec_eng', college='wse')]
        self.assertEqual(expected, get_education_records_for_student(test_student_data, test_dept_college_data))

    def test_ksas_freshman_with_defined_major(self):
        test_student_data = {
            'majors': ['B.A.: English'],
            'school_year': 'Freshman',
        }

        test_dept_college_data = {
            'B.A.: English': EducationRecord(
                major='B.A.: English',
                department='lit_lang_film',
                college='ksas'
            )
        }

        expected = [EducationRecord(major='English', department='lit_lang_film', college='ksas')]
        self.assertEqual(expected, get_education_records_for_student(test_student_data, test_dept_college_data))

    def test_freshman_with_undefined_major(self):
        test_student_data = {
            'majors': ['B.A.: Pre-Major', 'B.S.: Und Eng'],
            'school_year': 'Freshman',
        }

        test_dept_college_data = {
            'B.A.: Pre-Major': EducationRecord(major='B.A.: Pre-Major', department='soar_fye_ksas', college='ksas'),
            'B.S.: Und Eng': EducationRecord(major='B.S.: Und Eng', department='soar_fye_wse', college='wse'),
        }

        expected = [EducationRecord(major='Pre-Major', department='soar_fye_ksas', college='ksas'),
                    EducationRecord(major='Und Eng', department='soar_fye_wse', college='wse')]
        self.assertEqual(expected, get_education_records_for_student(test_student_data, test_dept_college_data))
