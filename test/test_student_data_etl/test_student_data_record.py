import unittest

from src.data_model import Departments
from src.student_data_etl.student_data_record import StudentRecord, EducationRecord


class TestStudentRecordUpdatesUniqueColleges(unittest.TestCase):

    def test_initializes_correctly_with_no_data(self):
        test_record = StudentRecord()
        self.assertEqual([], test_record.colleges)

    def test_initializes_correctly_with_one_education_record(self):
        test_record1 = StudentRecord(education_data=[EducationRecord(college='wse')])
        self.assertEqual(['wse'], test_record1.colleges)
        test_record2 = StudentRecord(education_data=[EducationRecord()])
        self.assertEqual([], test_record2.colleges)

    def test_initializes_correctly_with_multiple_records(self):
        test_record = StudentRecord(education_data=[EducationRecord(college='wse'), EducationRecord(),
                                                    EducationRecord(college='ksas')])
        self.assertEqual(['wse', 'ksas'], test_record.colleges)

    def test_adds_record_after_initialization(self):
        test_record = StudentRecord()
        test_record.add_education_record(EducationRecord(college='wse'))
        self.assertEqual(['wse'], test_record.colleges)

    def test_adds_duplicate_colleges(self):
        test_record = StudentRecord()
        test_record.add_education_record(EducationRecord(college='wse'))
        test_record.add_education_record(EducationRecord(college='wse'))
        self.assertEqual(['wse'], test_record.colleges)
        test_record.add_education_record(EducationRecord(college='ksas'))
        self.assertEqual(['wse', 'ksas'], test_record.colleges)
        test_record.add_education_record(EducationRecord(college='ksas'))
        self.assertEqual(['wse', 'ksas'], test_record.colleges)


class TestStudentRecordUpdatesUniqueMajors(unittest.TestCase):

    def test_initializes_correctly_with_no_data(self):
        test_record = StudentRecord()
        self.assertEqual([], test_record.majors)

    def test_initializes_correctly_with_one_education_record(self):
        test_record1 = StudentRecord(education_data=[EducationRecord(major='English')])
        self.assertEqual(['English'], test_record1.majors)
        test_record2 = StudentRecord(education_data=[EducationRecord()])
        self.assertEqual([], test_record2.majors)

    def test_add_majors_after_initialization_with_duplicates(self):
        test_record = StudentRecord()
        test_record.add_education_record(EducationRecord(major='English'))
        test_record.add_education_record(EducationRecord(major='English'))
        self.assertEqual(['English'], test_record.majors)
        test_record.add_education_record(EducationRecord(major='Comp Sci'))
        self.assertEqual(['English', 'Comp Sci'], test_record.majors)
        test_record.add_education_record(EducationRecord(major='Comp Sci'))
        self.assertEqual(['English', 'Comp Sci'], test_record.majors)


class TestStudentRecordUpdatesUniqueDepartments(unittest.TestCase):

    def test_initializes_correctly_with_no_data(self):
        test_record = StudentRecord()
        self.assertEqual([], test_record.departments)

    def test_initializes_correctly_with_one_education_record(self):
        test_record1 = StudentRecord(education_data=[EducationRecord(department='misc_eng')])
        self.assertEqual(['misc_eng'], test_record1.departments)
        test_record2 = StudentRecord(education_data=[EducationRecord()])
        self.assertEqual([], test_record2.departments)

    def test_add_departments_after_initialization_with_duplicates(self):
        test_record = StudentRecord()
        test_record.add_education_record(EducationRecord(department='misc_eng'))
        test_record.add_education_record(EducationRecord(department='misc_eng'))
        self.assertEqual(['misc_eng'], test_record.departments)
        test_record.add_education_record(EducationRecord(department='lit_lang_film'))
        self.assertEqual(['misc_eng', 'lit_lang_film'], test_record.departments)
        test_record.add_education_record(EducationRecord(department='lit_lang_film'))
        self.assertEqual(['misc_eng', 'lit_lang_film'], test_record.departments)

    def test_add_additional_departments_updates_additional_departments_list(self):
        test_record = StudentRecord()
        test_record.add_additional_department('soar_fye_ksas')
        self.assertEqual(['soar_fye_ksas'], test_record.additional_departments)
        test_record.add_additional_department('soar_fye_ksas')
        test_record.add_additional_department('soar_athletics')
        self.assertEqual(['soar_fye_ksas', 'soar_athletics'], test_record.additional_departments)

    def test_add_additional_departments_also_updates_departments(self):
        test_record = StudentRecord()
        test_record.add_education_record(EducationRecord(department='misc_eng'))
        test_record.add_additional_department('soar_fye_ksas')
        self.assertEqual(['soar_fye_ksas'], test_record.additional_departments)
        self.assertEqual(['misc_eng', 'soar_fye_ksas'], test_record.departments)
        test_record.add_additional_department('misc_eng')
        self.assertEqual(['misc_eng', 'soar_fye_ksas'], test_record.departments)

    def test_initialize_with_additional_departments(self):
        test_record = StudentRecord(additional_departments=['soar_fye_ksas'])
        self.assertEqual(['soar_fye_ksas'], test_record.additional_departments)
        self.assertEqual(['soar_fye_ksas'], test_record.departments)


class TestStudentRecordAthleteData(unittest.TestCase):

    def test_athlete_status_and_sports_initialize_correctly(self):
        test_record = StudentRecord()
        self.assertEqual([], test_record.sports)
        self.assertFalse(test_record.is_athlete)

    def test_adding_sport_sets_athlete_flag_and_updates_sports_list(self):
        test_record = StudentRecord()
        self.assertFalse(test_record.is_athlete)
        test_record.add_sport('Soccer')
        self.assertTrue(test_record.is_athlete)
        self.assertEqual(['Soccer'], test_record.sports)

        test_record.add_sport('Field Hockey')
        self.assertTrue(test_record.is_athlete)
        self.assertEqual(['Soccer', 'Field Hockey'], test_record.sports)

    def test_adding_duplicate_sport_does_nothing(self):
        test_record = StudentRecord()
        test_record.add_sport('Soccer')
        self.assertEqual(['Soccer'], test_record.sports)
        test_record.add_sport('Soccer')
        self.assertEqual(['Soccer'], test_record.sports)

    def test_initialize_with_sports_teams(self):
        test_record = StudentRecord(sports=['Soccer'])
        self.assertTrue(test_record.is_athlete)
        self.assertEqual(['Soccer'], test_record.sports)

    def test_adding_sport_also_adds_athlete_department(self):
        test_record = StudentRecord()
        self.assertEqual([], test_record.additional_departments)
        self.assertEqual([], test_record.departments)
        test_record.add_sport('Soccer')
        self.assertEqual([Departments.SOAR_ATHLETICS.value.name], test_record.additional_departments)
        self.assertEqual([Departments.SOAR_ATHLETICS.value.name], test_record.departments)
        test_record.add_sport('Field Hockey')
        self.assertEqual([Departments.SOAR_ATHLETICS.value.name], test_record.additional_departments)
        self.assertEqual([Departments.SOAR_ATHLETICS.value.name], test_record.departments)


class TestToDict(unittest.TestCase):

    def setUp(self):
        self.test_record = StudentRecord(
            handshake_username='astudent14',
            handshake_id='RT37H5',
            email='astudent14@jhu.edu',
            first_name='Angelica',
            pref_name='Angie',
            last_name='Student',
            school_year='Sophomore',
            education_data=[
                EducationRecord(major='English', department='lit_lang_film', college='ksas'),
                EducationRecord(major='Data Science', department='misc_eng', college='wse')
            ],
            additional_departments=['soar_athletics']
        )

    def test_plain_to_dict_method(self):
        expected = {
            'handshake_username': 'astudent14',
            'handshake_id': 'RT37H5',
            'email': 'astudent14@jhu.edu',
            'first_name': 'Angelica',
            'pref_name': 'Angie',
            'last_name': 'Student',
            'school_year': 'Sophomore',
            'education_records': [
                EducationRecord(major='English', department='lit_lang_film', college='ksas'),
                EducationRecord(major='Data Science', department='misc_eng', college='wse')
            ],
            'additional_departments': ['soar_athletics'],
            'is_athlete': False,
            'sports': [],
            'majors': ['English', 'Data Science'],
            'colleges': ['ksas', 'wse'],
            'departments': ['lit_lang_film', 'misc_eng', 'soar_athletics']
        }
        self.assertEqual(expected, self.test_record.to_dict())

    def test_to_dict_method_with_specified_fields(self):
        expected = {
            'email': 'astudent14@jhu.edu',
            'pref_name': 'Angie',
            'school_year': 'Sophomore',
            'education_records': [
                EducationRecord(major='English', department='lit_lang_film', college='ksas'),
                EducationRecord(major='Data Science', department='misc_eng', college='wse')
            ],
            'colleges': ['ksas', 'wse'],
        }
        specified_fields = ['email', 'pref_name', 'school_year', 'education_records', 'colleges']
        self.assertEqual(expected, self.test_record.to_dict(specified_fields))
