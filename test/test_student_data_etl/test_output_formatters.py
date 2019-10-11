import unittest

from src.student_data_etl.output_formatters import format_for_roster_file, format_for_data_file
from src.student_data_etl.student_data_record import StudentRecord, EducationRecord


class TestFormatForRosterFile(unittest.TestCase):

    def test_blank_record(self):
        test_record = StudentRecord()
        expected = [{
            'handshake_id': '',
            'email': '',
            'first_name': '',
            'pref_name': '',
            'last_name': '',
            'school_year': '',
            'department': '',
            'is_athlete': False,
            'sports': '',
            'majors': '',
            'colleges': ''
        }]
        self.assertEqual(expected, format_for_roster_file([test_record]))

    def test_record_with_one_complete_education_record(self):
        test_record = StudentRecord(
            handshake_username='49gj40',
            handshake_id='29384039',
            email='astu34@jhu.edu',
            first_name='Arthur',
            pref_name='Art',
            last_name='Stuart',
            school_year='Sophomore',
            education_data=[
                EducationRecord(major='Computer Science', department='comp_elec_eng', college='wse'),
            ]
        )
        expected = [{
            'handshake_id': '29384039',
            'email': 'astu34@jhu.edu',
            'first_name': 'Arthur',
            'pref_name': 'Art',
            'last_name': 'Stuart',
            'school_year': 'Sophomore',
            'department': 'comp_elec_eng',
            'is_athlete': False,
            'sports': '',
            'majors': 'Computer Science',
            'colleges': 'wse'
        }]
        self.assertEqual(expected, format_for_roster_file([test_record]))

    def test_record_with_incomplete_education_record(self):
        test_records = [
            StudentRecord(
                handshake_username='49gj40',
                handshake_id='29384039',
                email='astu34@jhu.edu',
                first_name='Arthur',
                pref_name='Art',
                last_name='Stuart',
                school_year='Sophomore',
                education_data=[
                    EducationRecord(major='Und A&S', department=None, college='ksas'),
                ]
            ),
            StudentRecord(
                handshake_username='t64453',
                handshake_id='16364533',
                email='bsmit15@jhu.edu',
                first_name='Brienne',
                last_name='Smith',
                school_year='Masters',
                sports=['Ice Hockey']
            )
        ]
        expected = [
            {
                'handshake_id': '29384039',
                'email': 'astu34@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Stuart',
                'school_year': 'Sophomore',
                'department': '',
                'is_athlete': False,
                'sports': '',
                'majors': 'Und A&S',
                'colleges': 'ksas'
            },
            {
                'handshake_id': '16364533',
                'email': 'bsmit15@jhu.edu',
                'first_name': 'Brienne',
                'pref_name': '',
                'last_name': 'Smith',
                'school_year': 'Masters',
                'department': 'soar_athletics',
                'is_athlete': True,
                'sports': 'Ice Hockey',
                'majors': '',
                'colleges': ''
            },
        ]
        self.assertEqual(expected, format_for_roster_file(test_records))

    def test_record_with_full_data(self):
        test_record = StudentRecord(
            handshake_username='49gj40',
            handshake_id='29384039',
            email='astu34@jhu.edu',
            first_name='Arthur',
            pref_name='Art',
            last_name='Stuart',
            school_year='Sophomore',
            education_data=[
                EducationRecord(major='Computer Science', department='comp_elec_eng', college='wse'),
                EducationRecord(major='English', department='lit_lang_film', college='ksas'),
                EducationRecord(major='Electrical Eng', department='comp_elec_eng', college='wse')
            ],
            sports=['Soccer', 'Lacrosse']
        )
        expected = [
            {
                'handshake_id': '29384039',
                'email': 'astu34@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Stuart',
                'school_year': 'Sophomore',
                'department': 'comp_elec_eng',
                'is_athlete': True,
                'sports': 'Soccer; Lacrosse',
                'majors': 'Computer Science; English; Electrical Eng',
                'colleges': 'wse; ksas'
            },
            {
                'handshake_id': '29384039',
                'email': 'astu34@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Stuart',
                'school_year': 'Sophomore',
                'department': 'lit_lang_film',
                'is_athlete': True,
                'sports': 'Soccer; Lacrosse',
                'majors': 'Computer Science; English; Electrical Eng',
                'colleges': 'wse; ksas'
            },
            {
                'handshake_id': '29384039',
                'email': 'astu34@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Stuart',
                'school_year': 'Sophomore',
                'department': 'soar_athletics',
                'is_athlete': True,
                'sports': 'Soccer; Lacrosse',
                'majors': 'Computer Science; English; Electrical Eng',
                'colleges': 'wse; ksas'
            },
        ]
        self.assertEqual(expected, format_for_roster_file([test_record]))

    def test_multiple_records(self):
        test_records = [
            StudentRecord(
                handshake_username='49gj40',
                handshake_id='29384039',
                email='astu34@jhu.edu',
                first_name='Arthur',
                pref_name='Art',
                last_name='Stuart',
                school_year='Sophomore',
                education_data=[
                    EducationRecord(major='Computer Science', department='comp_elec_eng', college='wse'),
                    EducationRecord(major='English', department='lit_lang_film', college='ksas'),
                    EducationRecord(major='Electrical Eng', department='comp_elec_eng', college='wse')
                ],
                sports=['Soccer', 'Lacrosse']
            ),
            StudentRecord(
                handshake_username='t64453',
                handshake_id='16364533',
                email='bsmit15@jhu.edu',
                first_name='Brienne',
                last_name='Smith',
                school_year='Masters',
                education_data=[
                    EducationRecord(major='M.S.E.: Data Science', department='ams_fm_data_science', college='wse'),
                ]
            )
        ]
        expected = [
            {
                'handshake_id': '29384039',
                'email': 'astu34@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Stuart',
                'school_year': 'Sophomore',
                'department': 'comp_elec_eng',
                'is_athlete': True,
                'sports': 'Soccer; Lacrosse',
                'majors': 'Computer Science; English; Electrical Eng',
                'colleges': 'wse; ksas'
            },
            {
                'handshake_id': '29384039',
                'email': 'astu34@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Stuart',
                'school_year': 'Sophomore',
                'department': 'lit_lang_film',
                'is_athlete': True,
                'sports': 'Soccer; Lacrosse',
                'majors': 'Computer Science; English; Electrical Eng',
                'colleges': 'wse; ksas'
            },
            {
                'handshake_id': '29384039',
                'email': 'astu34@jhu.edu',
                'first_name': 'Arthur',
                'pref_name': 'Art',
                'last_name': 'Stuart',
                'school_year': 'Sophomore',
                'department': 'soar_athletics',
                'is_athlete': True,
                'sports': 'Soccer; Lacrosse',
                'majors': 'Computer Science; English; Electrical Eng',
                'colleges': 'wse; ksas'
            },
            {
                'handshake_id': '16364533',
                'email': 'bsmit15@jhu.edu',
                'first_name': 'Brienne',
                'pref_name': '',
                'last_name': 'Smith',
                'school_year': 'Masters',
                'department': 'ams_fm_data_science',
                'is_athlete': False,
                'sports': '',
                'majors': 'M.S.E.: Data Science',
                'colleges': 'wse'
            },
        ]
        self.assertEqual(expected, format_for_roster_file(test_records))


class TestFormatForDataFile(unittest.TestCase):

    def test_blank_record(self):
        test_record = StudentRecord()
        expected = [{
            'handshake_username': '',
            'handshake_id': '',
            'major': '',
            'school_year': '',
            'department': '',
            'college': '',
            'is_athlete': False,
            'sport': ''
        }]
        self.assertEqual(expected, format_for_data_file([test_record]))

    def test_record_with_one_complete_education_record(self):
        test_record = StudentRecord(
            handshake_username='49gj40',
            handshake_id='29384039',
            email='astu34@jhu.edu',
            first_name='Arthur',
            pref_name='Art',
            last_name='Stuart',
            school_year='Sophomore',
            education_data=[
                EducationRecord(major='Computer Science', department='comp_elec_eng', college='wse'),
            ]
        )
        expected = [{
            'handshake_username': '49gj40',
            'handshake_id': '29384039',
            'major': 'Computer Science',
            'school_year': 'Sophomore',
            'department': 'comp_elec_eng',
            'college': 'wse',
            'is_athlete': False,
            'sport': ''
        }]
        self.assertEqual(expected, format_for_data_file([test_record]))

    def test_full_record_with_additional_departments_and_sports(self):
        test_record = StudentRecord(
            handshake_username='49gj40',
            handshake_id='29384039',
            email='astu34@jhu.edu',
            first_name='Arthur',
            pref_name='Art',
            last_name='Stuart',
            school_year='Freshman',
            education_data=[
                EducationRecord(major='Computer Science', department='comp_elec_eng', college='wse'),
                EducationRecord(major='English', department='lit_lang_film', college='ksas')
            ],
            sports=['Soccer', 'Lacrosse'],
            additional_departments=['soar_fye_wse']
        )
        expected = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '29384039',
                'major': 'Computer Science',
                'school_year': 'Freshman',
                'department': 'soar_fye_wse',
                'college': 'wse',
                'is_athlete': True,
                'sport': 'Soccer'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '29384039',
                'major': 'Computer Science',
                'school_year': 'Freshman',
                'department': 'soar_fye_wse',
                'college': 'wse',
                'is_athlete': True,
                'sport': 'Lacrosse'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '29384039',
                'major': 'Computer Science',
                'school_year': 'Freshman',
                'department': 'soar_athletics',
                'college': 'wse',
                'is_athlete': True,
                'sport': 'Soccer'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '29384039',
                'major': 'Computer Science',
                'school_year': 'Freshman',
                'department': 'soar_athletics',
                'college': 'wse',
                'is_athlete': True,
                'sport': 'Lacrosse'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '29384039',
                'major': 'Computer Science',
                'school_year': 'Freshman',
                'department': 'comp_elec_eng',
                'college': 'wse',
                'is_athlete': True,
                'sport': 'Soccer'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '29384039',
                'major': 'Computer Science',
                'school_year': 'Freshman',
                'department': 'comp_elec_eng',
                'college': 'wse',
                'is_athlete': True,
                'sport': 'Lacrosse'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '29384039',
                'major': 'English',
                'school_year': 'Freshman',
                'department': 'soar_fye_wse',
                'college': 'ksas',
                'is_athlete': True,
                'sport': 'Soccer'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '29384039',
                'major': 'English',
                'school_year': 'Freshman',
                'department': 'soar_fye_wse',
                'college': 'ksas',
                'is_athlete': True,
                'sport': 'Lacrosse'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '29384039',
                'major': 'English',
                'school_year': 'Freshman',
                'department': 'soar_athletics',
                'college': 'ksas',
                'is_athlete': True,
                'sport': 'Soccer'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '29384039',
                'major': 'English',
                'school_year': 'Freshman',
                'department': 'soar_athletics',
                'college': 'ksas',
                'is_athlete': True,
                'sport': 'Lacrosse'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '29384039',
                'major': 'English',
                'school_year': 'Freshman',
                'department': 'lit_lang_film',
                'college': 'ksas',
                'is_athlete': True,
                'sport': 'Soccer'
            },
            {
                'handshake_username': '49gj40',
                'handshake_id': '29384039',
                'major': 'English',
                'school_year': 'Freshman',
                'department': 'lit_lang_film',
                'college': 'ksas',
                'is_athlete': True,
                'sport': 'Lacrosse'
            },
        ]
        self.assertEqual(expected, format_for_data_file([test_record]))

    def test_multiple_records(self):
        test_records = [
            StudentRecord(
                handshake_username='49gj40',
                handshake_id='29384039',
                email='astu34@jhu.edu',
                first_name='Arthur',
                pref_name='Art',
                last_name='Stuart',
                school_year='Sophomore',
                education_data=[
                    EducationRecord(major='Biomedical Engineering', department='bme', college='wse'),
                ]
            ),
            StudentRecord(
                handshake_username='627745',
                handshake_id='928379843',
                email='bsmit15@jhu.edu',
                school_year='Senior',
                education_data=[
                    EducationRecord(major='Computer Science', department='comp_elec_eng', college='wse'),
                    EducationRecord(major='Electrical Engineering', department='comp_elec_eng', college='wse')
                ]
            )
        ]
        expected = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '29384039',
                'major': 'Biomedical Engineering',
                'school_year': 'Sophomore',
                'department': 'bme',
                'college': 'wse',
                'is_athlete': False,
                'sport': ''
            },
            {
                'handshake_username': '627745',
                'handshake_id': '928379843',
                'major': 'Computer Science',
                'school_year': 'Senior',
                'department': 'comp_elec_eng',
                'college': 'wse',
                'is_athlete': False,
                'sport': ''
            },
            {
                'handshake_username': '627745',
                'handshake_id': '928379843',
                'major': 'Electrical Engineering',
                'school_year': 'Senior',
                'department': 'comp_elec_eng',
                'college': 'wse',
                'is_athlete': False,
                'sport': ''
            },

        ]
        self.assertEqual(expected, format_for_data_file(test_records))

    def test_incomplete_records(self):
        test_records = [
            StudentRecord(
                handshake_username='49gj40',
                handshake_id='29384039',
                email='astu34@jhu.edu',
                first_name='Arthur',
                pref_name='Art',
                last_name='Stuart',
                school_year='Sophomore',
                education_data=[
                    EducationRecord(major='Biomedical Engineering', department=None, college='wse'),
                ]
            ),
            StudentRecord(
                handshake_username='627745',
                handshake_id='928379843',
                email='bsmit15@jhu.edu',
                school_year='Senior',
                additional_departments=['soar_fye_wse']
            )
        ]
        expected = [
            {
                'handshake_username': '49gj40',
                'handshake_id': '29384039',
                'major': 'Biomedical Engineering',
                'school_year': 'Sophomore',
                'department': '',
                'college': 'wse',
                'is_athlete': False,
                'sport': ''
            },
            {
                'handshake_username': '627745',
                'handshake_id': '928379843',
                'major': '',
                'school_year': 'Senior',
                'department': 'soar_fye_wse',
                'college': '',
                'is_athlete': False,
                'sport': ''
            }
        ]
        self.assertEqual(expected, format_for_data_file(test_records))
