import unittest

from src.student_data_etl.output_formatters import format_for_roster_file
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
