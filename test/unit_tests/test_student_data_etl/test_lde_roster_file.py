import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from src.student_data_etl.lde_roster_file import split_into_separate_department_rosters
from src.student_data_etl.lde_roster_file import unmelt_and_join
from src.student_data_etl.lde_roster_file import unmelt_students_for_roster_file


class TestUnmeltStudentsForRosterFile(unittest.TestCase):

    def test_unmelts_major_college_and_department_without_creating_duplicates(self):
        students = pd.DataFrame({
            'hopkins_id': ['8fj4t2', '8fj4t2'],
            'other_field': [0, 1],
            'major': ['english', 'physics'],
            'college': ['ksas', 'wse'],
            'department': ['humanities', 'phys_sci']
        })

        expected = pd.DataFrame({
            'hopkins_id': ['8fj4t2', '8fj4t2'],
            'other_field': [0, 1],
            'department': ['humanities', 'phys_sci'],
            'majors': ['english;physics', 'english;physics'],
            'colleges': ['ksas;wse', 'ksas;wse'],
            'departments': ['humanities;phys_sci', 'humanities;phys_sci']
        })

        assert_frame_equal(expected, unmelt_students_for_roster_file(students))

    def test_removes_duplicates_that_are_already_present_in_the_input_data(self):
        students = pd.DataFrame({
            'hopkins_id': ['8fj4t2', '8fj4t2'],
            'other_field': [0, 0],
            'major': ['english', 'english'],
            'college': ['ksas', 'ksas'],
            'department': ['humanities', 'humanities']
        })

        expected = pd.DataFrame({
            'hopkins_id': ['8fj4t2'],
            'other_field': [0],
            'department': ['humanities'],
            'majors': ['english'],
            'colleges': ['ksas'],
            'departments': ['humanities']
        })

        assert_frame_equal(expected, unmelt_students_for_roster_file(students))


class TestUnmeltAndJoin(unittest.TestCase):

    def test_only_changes_the_column_name_if_a_student_only_has_a_single_row_to_begin_with(self):
        students = pd.DataFrame({'hopkins_id': ['8fj4t2'], 'other_field': [1], 'melted_field': ['value1']})
        expected = pd.DataFrame({
            'hopkins_id': ['8fj4t2'],
            'other_field': [1],
            'melted_field': ['value1'],
            'unmelted_field': ['value1']
        })
        assert_frame_equal(expected, unmelt_and_join(students, 'melted_field', 'unmelted_field'))

    def test_concatenates_all_values_in_the_column_to_unmelt_and_merges_the_resulting_string_back_onto_the_student_df(self):
        students = pd.DataFrame({'hopkins_id': ['8fj4t2', '8fj4t2'], 'other_field': [1, 0], 'melted_field': ['value1', 'value2']})
        expected = pd.DataFrame({
            'hopkins_id': ['8fj4t2', '8fj4t2'],
            'other_field': [1, 0],
            'melted_field': ['value1', 'value2'],
            'unmelted_field': ['value1;value2', 'value1;value2']
        })
        assert_frame_equal(expected, unmelt_and_join(students, 'melted_field', 'unmelted_field'))

    def test_only_concatenates_unique_values_in_the_column_to_unmelt(self):
        students = pd.DataFrame({'hopkins_id': ['8fj4t2', '8fj4t2'], 'other_field': [1, 0], 'melted_field': ['value1', 'value1']})
        expected = pd.DataFrame({
            'hopkins_id': ['8fj4t2', '8fj4t2'],
            'other_field': [1, 0],
            'melted_field': ['value1', 'value1'],
            'unmelted_field': ['value1', 'value1']
        })
        assert_frame_equal(expected, unmelt_and_join(students, 'melted_field', 'unmelted_field'))

    def test_unmelts_using_hopkins_id_as_the_id(self):
        students = pd.DataFrame({'hopkins_id': ['8fj4t2', 'pap9f3', '8fj4t2'], 'other_field': [1, 0, 0], 'melted_field': ['value1', 'value3', 'value2']})
        expected = pd.DataFrame({
            'hopkins_id': ['8fj4t2', 'pap9f3', '8fj4t2'],
            'other_field': [1, 0, 0],
            'melted_field': ['value1', 'value3', 'value2'],
            'unmelted_field': ['value1;value2', 'value3', 'value1;value2']
        })
        assert_frame_equal(expected, unmelt_and_join(students, 'melted_field', 'unmelted_field'))

    def test_converts_entirely_null_column_to_the_empty_string(self):
        students = pd.DataFrame({'hopkins_id': ['8fj4t2'], 'other_field': [1], 'melted_field': [None]})
        expected = pd.DataFrame({
            'hopkins_id': ['8fj4t2'],
            'other_field': [1],
            'melted_field': [None],
            'unmelted_field': ['']
        })
        assert_frame_equal(expected, unmelt_and_join(students, 'melted_field', 'unmelted_field'))

    def test_ignores_nulls_intermixed_among_real_values(self):
        students = pd.DataFrame({'hopkins_id': ['8fj4t2', 'pap9f3', '8fj4t2'], 'other_field': [1, 0, 0], 'melted_field': [None, None, 'value2']})
        expected = pd.DataFrame({
            'hopkins_id': ['8fj4t2', 'pap9f3', '8fj4t2'],
            'other_field': [1, 0, 0],
            'melted_field': [None, None, 'value2'],
            'unmelted_field': ['value2', '', 'value2']
        })
        assert_frame_equal(expected, unmelt_and_join(students, 'melted_field', 'unmelted_field'))

    def test_ignores_empty_strings_intermixed_among_real_values(self):
        students = pd.DataFrame({'hopkins_id': ['8fj4t2', 'pap9f3', '8fj4t2'], 'other_field': [1, 0, 0], 'melted_field': ['', '', 'value2']})
        expected = pd.DataFrame({
            'hopkins_id': ['8fj4t2', 'pap9f3', '8fj4t2'],
            'other_field': [1, 0, 0],
            'melted_field': ['', '', 'value2'],
            'unmelted_field': ['value2', '', 'value2']
        })
        assert_frame_equal(expected, unmelt_and_join(students, 'melted_field', 'unmelted_field'))


class TestSplitIntoSeparateDepartmentRosters(unittest.TestCase):

    def test_creates_a_separate_dataframe_for_each_department(self):
        roster = pd.DataFrame({
            'hopkins_id': ['8fj4t2', '8fj4t2', 'sfs834'],
            'other_field': [0, 1, 2],
            'department': ['humanities', 'phys_sci', 'humanities'],
        })
        expected = [
            pd.DataFrame({
                'hopkins_id': ['8fj4t2', 'sfs834'],
                'other_field': [0, 2],
                'department': ['humanities', 'humanities'],
            }),
            pd.DataFrame({
                'hopkins_id': ['8fj4t2'],
                'other_field': [1],
                'department': ['phys_sci'],
            })
        ]
        actual = split_into_separate_department_rosters(roster)
        for i in range(len(expected)):
            assert_frame_equal(expected[i], actual[i])

    def test_puts_all_rows_with_null_dept_into_special_no_department_roster(self):
        roster = pd.DataFrame({
            'hopkins_id': ['8fj4t2'],
            'department': [None],
        })
        actual = split_into_separate_department_rosters(roster)
        expected = [
            pd.DataFrame({
                'hopkins_id': ['8fj4t2'],
                'department': ['no_department'],
            })
        ]
        for i in range(len(expected)):
            assert_frame_equal(expected[i], actual[i])