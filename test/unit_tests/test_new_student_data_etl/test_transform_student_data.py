import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from src.data_model import Departments
from src.new_student_data_etl.transform_student_data import add_major_metadata
from src.new_student_data_etl.transform_student_data import make_student_department_subtable
from src.new_student_data_etl.transform_student_data import make_student_department_table
from src.new_student_data_etl.transform_student_data import melt_majors
from src.new_student_data_etl.transform_student_data import clean_majors
from src.new_student_data_etl.transform_student_data import merge_with_handshake_data
from src.new_student_data_etl.transform_student_data import merge_with_student_department_data
from src.new_student_data_etl.transform_student_data import merge_with_engagement_data


class TestCleanMajor(unittest.TestCase):

    def test_major_without_colon_is_not_changed(self):
        students = pd.DataFrame({'major': ['economics']})
        expected = pd.DataFrame({'major': ['economics']})
        assert_frame_equal(expected, clean_majors(students))

    def test_major_starting_with_m_dot_is_not_changed(self):
        students = pd.DataFrame({'major': ['M.S.: economics']})
        expected = pd.DataFrame({'major': ['M.S.: economics']})
        assert_frame_equal(expected, clean_majors(students))

    def test_major_starting_with_phd_is_not_changed(self):
        students = pd.DataFrame({'major': ['Ph.D.: economics']})
        expected = pd.DataFrame({'major': ['Ph.D.: economics']})
        assert_frame_equal(expected, clean_majors(students))

    def test_otherwise_any_text_before_the_first_colon_is_discarded(self):
        students = pd.DataFrame({'major': ['B.A.: economics']})
        expected = pd.DataFrame({'major': ['economics']})
        assert_frame_equal(expected, clean_majors(students))


class TestAddMajorMetadata(unittest.TestCase):

    def test_left_joins_student_data_to_major_metadata_using_major_as_the_join_key(self):
        students = pd.DataFrame({'major': ['economics', 'comp sci', 'economics']})
        major_metadata = pd.DataFrame({'major': ['economics', 'comp sci'], 'college': ['ksas', 'wse'], 'department': ['pol_sci_econ', 'comp_elec_eng']})
        expected = pd.DataFrame({
            'major': ['economics', 'comp sci', 'economics'],
            'college': ['ksas', 'wse', 'ksas'],
            'major_department': ['pol_sci_econ', 'comp_elec_eng', 'pol_sci_econ']
        })
        assert_frame_equal(expected, add_major_metadata(students, major_metadata))


class TestMeltMajors(unittest.TestCase):

    def test_leaves_row_with_only_one_major_unchanged_except_for_the_column_name(self):
        students = pd.DataFrame({'hopkins_id': ['fi9485'], 'majors': ['economics']})
        expected = pd.DataFrame({'hopkins_id': ['fi9485'], 'major': ['economics']})
        assert_frame_equal(expected, melt_majors(students))

    def test_splits_major_string_into_separate_columns_and_unpivots_those_columns_into_a_single_major_column(self):
        students = pd.DataFrame({'hopkins_id': ['uu9d32'], 'majors': ['economics;math;science']})
        expected = pd.DataFrame({'hopkins_id': ['uu9d32', 'uu9d32', 'uu9d32'], 'major': ['economics', 'math', 'science']})
        assert_frame_equal(expected, melt_majors(students))

    def test_only_includes_rows_for_non_null_majors(self):
        students = pd.DataFrame({'hopkins_id': ['uu9d32', '938tjg'], 'majors': ['economics;math;science', 'english']})
        expected = pd.DataFrame({'hopkins_id': ['uu9d32', 'uu9d32', 'uu9d32', '938tjg'], 'major': ['economics', 'math', 'science', 'english']})
        assert_frame_equal(expected, melt_majors(students))


class TestMergeWithHandshakeData(unittest.TestCase):

    def test_merges_student_data_with_handshake_data_on_jhed(self):
        students = pd.DataFrame({'jhed': ['asmi34', 'asmi34', 'bmart15']})
        handshake_data = pd.DataFrame({'jhed': ['asmi34', 'bmart15'], 'handshake_field': ['value1', 'value2']})
        expected = pd.DataFrame({
            'jhed': ['asmi34', 'asmi34', 'bmart15'],
            'handshake_field': ['value1', 'value1', 'value2']
        })
        assert_frame_equal(expected, merge_with_handshake_data(students, handshake_data))


class TestMergeWithEngagementData(unittest.TestCase):

    def test_merges_student_data_with_engagement_data_on_handshake_id(self):
        students = pd.DataFrame({'handshake_id': ['230942095', '10193853'], 'other_field': ['a', 'b']})
        engagement_data = pd.DataFrame({'student_handshake_id': ['230942095', '10193853'], 'event_engagement': [4, 2]})
        expected = pd.DataFrame({
            'handshake_id': ['230942095', '10193853'],
            'other_field': ['a', 'b'],
            'event_engagement': [4, 2],
        })
        assert_frame_equal(expected, merge_with_engagement_data(students, engagement_data))

    def test_fills_na_with_zero_for_students_with_no_engagement_data(self):
        students = pd.DataFrame({'handshake_id': ['230942095'], 'other_field': [None]})
        engagement_data = pd.DataFrame({'student_handshake_id': [], 'event_engagement': []})
        expected = pd.DataFrame({
            'handshake_id': ['230942095'],
            'other_field': [None],
            'event_engagement': [0],
        })
        assert_frame_equal(expected, merge_with_engagement_data(students, engagement_data))


class TestMergeWithStudentDepartmentData(unittest.TestCase):

    def test_merges_with_student_department_data_on_hopkins_id(self):
        students = pd.DataFrame({'hopkins_id': ['jf38ru', 'mmd09s']})
        student_departments = pd.DataFrame({
            'hopkins_id': ['jf38ru', 'mmd09s', 'jf38ru'],
            'department': ['pol_sci_econ', 'comp_elec_eng', 'humanities']
        })
        expected = pd.DataFrame({
            'hopkins_id': ['jf38ru', 'jf38ru', 'mmd09s'],
            'department': ['pol_sci_econ', 'humanities', 'comp_elec_eng']
        })
        assert_frame_equal(expected, merge_with_student_department_data(students, student_departments))


class TestMakeStudentDepartmentsSubTable(unittest.TestCase):

    def test_makes_an_empty_dataframe_if_the_given_hopkins_id_does_not_appear_in_the_students_table(self):
        students = pd.DataFrame({
            'hopkins_id': [],
            'college': [],
            'school_year': [],
            'is_athlete': [],
            'is_urm': [],
            'major_department': []
        })
        expected = pd.DataFrame({
            'hopkins_id': [],
            'department': []
        })
        assert_frame_equal(expected, make_student_department_subtable(students, 'invalid id'))

    def test_makes_a_dataframe_mapping_hopkins_id_to_academic_departments_if_student_doesnt_fall_into_any_soar_departments(self):
        students = pd.DataFrame({
            'hopkins_id': ['jf38ru', 'jf38ru', 'kf034i'],
            'college': ['ksas', 'wse', 'ksas'],
            'school_year': ['Senior', 'Senior', 'Junior'],
            'is_athlete': [False, False, False],
            'is_urm': [False, False, False],
            'major_department': ['pol_sci_econ', 'comp_elec_eng', 'pol_sci_econ']
        })
        expected = pd.DataFrame({
            'hopkins_id': ['jf38ru', 'jf38ru'],
            'department': ['pol_sci_econ', 'comp_elec_eng']
        })
        assert_frame_equal(expected, make_student_department_subtable(students, 'jf38ru'))

    def test_includes_soar_fye_ksas_department_for_ksas_freshmen_who_have_already_chosen_a_major(self):
        students = pd.DataFrame({
            'hopkins_id': ['93aml3'],
            'college': ['ksas'],
            'school_year': ['Freshman'],
            'is_athlete': [False],
            'is_urm': [False],
            'major_department': ['pol_sci_econ']
        })
        expected = pd.DataFrame({
            'hopkins_id': ['93aml3', '93aml3'],
            'department': ['pol_sci_econ', Departments.SOAR_FYE_KSAS.value.name]
        })
        assert_frame_equal(expected, make_student_department_subtable(students, '93aml3'))

    def test_only_includes_soar_fye_ksas_department_once_for_ksas_freshmen_who_have_not_chosen_a_major(self):
        students = pd.DataFrame({
            'hopkins_id': ['93aml3'],
            'college': ['ksas'],
            'school_year': ['Freshman'],
            'is_athlete': [False],
            'is_urm': [False],
            'major_department': [Departments.SOAR_FYE_KSAS.value.name]
        })
        expected = pd.DataFrame({
            'hopkins_id': ['93aml3'],
            'department': [Departments.SOAR_FYE_KSAS.value.name]
        })
        assert_frame_equal(expected, make_student_department_subtable(students, '93aml3'))

    def test_includes_soar_fye_wse_department_for_wse_freshmen_who_have_already_chosen_a_major(self):
        students = pd.DataFrame({
            'hopkins_id': ['93aml3'],
            'college': ['wse'],
            'school_year': ['Freshman'],
            'is_athlete': [False],
            'is_urm': [False],
            'major_department': ['comp_sci']
        })
        expected = pd.DataFrame({
            'hopkins_id': ['93aml3', '93aml3'],
            'department': ['comp_sci', Departments.SOAR_FYE_WSE.value.name]
        })
        assert_frame_equal(expected, make_student_department_subtable(students, '93aml3'))

    def test_includes_soar_athletics_department_for_athletes(self):
        students = pd.DataFrame({
            'hopkins_id': ['jf398f'],
            'college': ['wse'],
            'school_year': ['Sophomore'],
            'is_athlete': [True],
            'is_urm': [False],
            'major_department': ['comp_sci']
        })
        expected = pd.DataFrame({
            'hopkins_id': ['jf398f', 'jf398f'],
            'department': ['comp_sci', Departments.SOAR_ATHLETICS.value.name]
        })
        assert_frame_equal(expected, make_student_department_subtable(students, 'jf398f'))

    def test_includes_soar_diversity_and_inclusion_department_for_urms(self):
        students = pd.DataFrame({
            'hopkins_id': ['pmle45'],
            'college': ['wse'],
            'school_year': ['Sophomore'],
            'is_athlete': [False],
            'is_urm': [True],
            'major_department': ['elec_eng']
        })
        expected = pd.DataFrame({
            'hopkins_id': ['pmle45', 'pmle45'],
            'department': ['elec_eng', Departments.SOAR_DIV_INCL.value.name]
        })
        assert_frame_equal(expected, make_student_department_subtable(students, 'pmle45'))

    def test_includes_multiple_soar_departments_as_appropriate(self):
        students = pd.DataFrame({
            'hopkins_id': ['pmle45', 'pmle45'],
            'college': ['wse', 'ksas'],
            'school_year': ['Freshman', 'Freshman'],
            'is_athlete': [True, True],
            'is_urm': [True, True],
            'major_department': ['elec_eng', Departments.SOAR_FYE_KSAS.value.name]
        })
        expected = pd.DataFrame({
            'hopkins_id': ['pmle45', 'pmle45', 'pmle45', 'pmle45', 'pmle45'],
            'department': [
                'elec_eng',
                Departments.SOAR_FYE_KSAS.value.name,
                Departments.SOAR_FYE_WSE.value.name,
                Departments.SOAR_ATHLETICS.value.name,
                Departments.SOAR_DIV_INCL.value.name]
        })
        assert_frame_equal(expected, make_student_department_subtable(students, 'pmle45'))


class TestMakeStudentDepartmentsTable(unittest.TestCase):

    def test_makes_an_empty_dataframe_if_given_an_empty_student_table(self):
        students = pd.DataFrame({
            'hopkins_id': [],
            'college': [],
            'school_year': [],
            'is_athlete': [],
            'is_urm': [],
            'major_department': []
        })
        expected = pd.DataFrame({
            'hopkins_id': [],
            'department': []
        })
        assert_frame_equal(expected, make_student_department_table(students))

    def test_does_the_same_thing_as_subtable_if_there_is_only_one_student(self):
        students = pd.DataFrame({
            'hopkins_id': ['93aml3'],
            'college': ['ksas'],
            'school_year': ['Freshman'],
            'is_athlete': [False],
            'is_urm': [False],
            'major_department': ['pol_sci_econ']
        })
        expected = pd.DataFrame({
            'hopkins_id': ['93aml3', '93aml3'],
            'department': ['pol_sci_econ', Departments.SOAR_FYE_KSAS.value.name]
        })
        assert_frame_equal(expected, make_student_department_table(students))

    def test_makes_a_table_mapping_every_student_to_their_academic_and_soar_departments(self):
        students = pd.DataFrame({
            'hopkins_id': ['93aml3', 'ndfe83', '78576e'],
            'college': ['ksas', 'ksas', 'wse'],
            'school_year': ['Sophomore', 'Sophomore', 'Junior'],
            'is_athlete': [False, False, False],
            'is_urm': [False, False, False],
            'major_department': ['pol_sci_econ', 'brain_sci', 'comp_sci']
        })
        expected = pd.DataFrame({
            'hopkins_id': ['93aml3', 'ndfe83', '78576e'],
            'department': ['pol_sci_econ', 'brain_sci', 'comp_sci']
        })
        assert_frame_equal(expected, make_student_department_table(students))
