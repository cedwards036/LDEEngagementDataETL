import unittest

from src.student_data_etl.student_data_record import StudentDataRecord, EducationDataRecord


class TestStudentDataRecordUpdatesUniqueColleges(unittest.TestCase):

    def test_initializes_correctly_with_no_data(self):
        test_record = StudentDataRecord()
        self.assertEqual([], test_record.colleges)

    def test_initializes_correctly_with_one_education_record(self):
        test_record1 = StudentDataRecord(education_data=[EducationDataRecord(college='wse')])
        self.assertEqual(['wse'], test_record1.colleges)
        test_record2 = StudentDataRecord(education_data=[EducationDataRecord()])
        self.assertEqual([], test_record2.colleges)

    def test_initializes_correctly_with_multiple_records(self):
        test_record = StudentDataRecord(education_data=[EducationDataRecord(college='wse'), EducationDataRecord(),
                                                        EducationDataRecord(college='ksas')])
        self.assertEqual(['wse', 'ksas'], test_record.colleges)

    def test_adds_record_after_initialization(self):
        test_record = StudentDataRecord()
        test_record.add_education_record(EducationDataRecord(college='wse'))
        self.assertEqual(['wse'], test_record.colleges)

    def test_adds_duplicate_colleges(self):
        test_record = StudentDataRecord()
        test_record.add_education_record(EducationDataRecord(college='wse'))
        test_record.add_education_record(EducationDataRecord(college='wse'))
        self.assertEqual(['wse'], test_record.colleges)
        test_record.add_education_record(EducationDataRecord(college='ksas'))
        self.assertEqual(['wse', 'ksas'], test_record.colleges)
        test_record.add_education_record(EducationDataRecord(college='ksas'))
        self.assertEqual(['wse', 'ksas'], test_record.colleges)


class TestStudentDataRecordUpdatesUniqueMajors(unittest.TestCase):

    def test_initializes_correctly_with_no_data(self):
        test_record = StudentDataRecord()
        self.assertEqual([], test_record.majors)

    def test_initializes_correctly_with_one_education_record(self):
        test_record1 = StudentDataRecord(education_data=[EducationDataRecord(major='English')])
        self.assertEqual(['English'], test_record1.majors)
        test_record2 = StudentDataRecord(education_data=[EducationDataRecord()])
        self.assertEqual([], test_record2.majors)

    def test_add_majors_after_initialization_with_duplicates(self):
        test_record = StudentDataRecord()
        test_record.add_education_record(EducationDataRecord(major='English'))
        test_record.add_education_record(EducationDataRecord(major='English'))
        self.assertEqual(['English'], test_record.majors)
        test_record.add_education_record(EducationDataRecord(major='Comp Sci'))
        self.assertEqual(['English', 'Comp Sci'], test_record.majors)
        test_record.add_education_record(EducationDataRecord(major='Comp Sci'))
        self.assertEqual(['English', 'Comp Sci'], test_record.majors)


class TestStudentDataRecordUpdatesUniqueDepartments(unittest.TestCase):

    def test_initializes_correctly_with_no_data(self):
        test_record = StudentDataRecord()
        self.assertEqual([], test_record.departments)

    def test_initializes_correctly_with_one_education_record(self):
        test_record1 = StudentDataRecord(education_data=[EducationDataRecord(department='misc_eng')])
        self.assertEqual(['misc_eng'], test_record1.departments)
        test_record2 = StudentDataRecord(education_data=[EducationDataRecord()])
        self.assertEqual([], test_record2.departments)

    def test_add_departments_after_initialization_with_duplicates(self):
        test_record = StudentDataRecord()
        test_record.add_education_record(EducationDataRecord(department='misc_eng'))
        test_record.add_education_record(EducationDataRecord(department='misc_eng'))
        self.assertEqual(['misc_eng'], test_record.departments)
        test_record.add_education_record(EducationDataRecord(department='lit_lang_film'))
        self.assertEqual(['misc_eng', 'lit_lang_film'], test_record.departments)
        test_record.add_education_record(EducationDataRecord(department='lit_lang_film'))
        self.assertEqual(['misc_eng', 'lit_lang_film'], test_record.departments)

    def test_add_additional_departments_updates_additional_departments_list(self):
        test_record = StudentDataRecord()
        test_record.add_additional_department('soar_fye_ksas')
        self.assertEqual(['soar_fye_ksas'], test_record.additional_departments)
        test_record.add_additional_department('soar_fye_ksas')
        test_record.add_additional_department('soar_athletics')
        self.assertEqual(['soar_fye_ksas', 'soar_athletics'], test_record.additional_departments)

    def test_add_additional_departments_also_updates_departments(self):
        test_record = StudentDataRecord()
        test_record.add_education_record(EducationDataRecord(department='misc_eng'))
        test_record.add_additional_department('soar_fye_ksas')
        self.assertEqual(['soar_fye_ksas'], test_record.additional_departments)
        self.assertEqual(['misc_eng', 'soar_fye_ksas'], test_record.departments)
        test_record.add_additional_department('misc_eng')
        self.assertEqual(['misc_eng', 'soar_fye_ksas'], test_record.departments)

    def test_initialize_with_additional_departments(self):
        test_record = StudentDataRecord(additional_departments=['soar_fye_ksas'])
        self.assertEqual(['soar_fye_ksas'], test_record.additional_departments)
        self.assertEqual(['soar_fye_ksas'], test_record.departments)


class TestToDict(unittest.TestCase):

    def setUp(self):
        self.test_record = StudentDataRecord(
            handshake_username='astudent14',
            handshake_id='RT37H5',
            email='astudent14@jhu.edu',
            first_name='Angelica',
            pref_name='Angie',
            last_name='Student',
            school_year='Sophomore',
            education_data=[
                EducationDataRecord(major='English', department='lit_lang_film', college='ksas'),
                EducationDataRecord(major='Data Science', department='misc_eng', college='wse')
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
            'education_data': [
                EducationDataRecord(major='English', department='lit_lang_film', college='ksas'),
                EducationDataRecord(major='Data Science', department='misc_eng', college='wse')
            ],
            'additional_departments': ['soar_athletics'],
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
            'education_data': [
                EducationDataRecord(major='English', department='lit_lang_film', college='ksas'),
                EducationDataRecord(major='Data Science', department='misc_eng', college='wse')
            ],
            'colleges': ['ksas', 'wse'],
        }
        specified_fields = ['email', 'pref_name', 'school_year', 'education_data', 'colleges']
        self.assertEqual(expected, self.test_record.to_dict(specified_fields))
