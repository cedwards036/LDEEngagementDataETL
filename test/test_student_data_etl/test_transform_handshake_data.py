import unittest

import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from lde_etl.handshake_fields import StudentFields
from lde_etl.student_data_etl.transform_handshake_data import add_pre_med_column
from lde_etl.student_data_etl.transform_handshake_data import clean_logged_in_column
from lde_etl.student_data_etl.transform_handshake_data import clean_profile_completion_column
from lde_etl.student_data_etl.transform_handshake_data import convert_auth_id_to_jhed
from lde_etl.student_data_etl.transform_handshake_data import rename_handshake_id_column
from lde_etl.student_data_etl.transform_handshake_data import transform_handshake_data


class TestCleanLoggedInColumn(unittest.TestCase):

    def test_renames_logged_in_column(self):
        handshake_data = pd.DataFrame({StudentFields.HAS_LOGGED_IN: []})
        result = clean_logged_in_column(handshake_data)
        assert_column_was_renamed(self, result, StudentFields.HAS_LOGGED_IN, 'has_activated_handshake')

    def test_converts_yes_and_no_to_true_and_false_and_leaves_other_values_unchanged(self):
        handshake_data = pd.DataFrame({StudentFields.HAS_LOGGED_IN: ['Yes', 'No', None]})
        expected = pd.Series([True, False, None], name='has_activated_handshake')
        assert_series_equal(expected, clean_logged_in_column(handshake_data)['has_activated_handshake'])


class TestCleanProfileCompletionColumn(unittest.TestCase):

    def test_renames_logged_in_column(self):
        handshake_data = pd.DataFrame({StudentFields.HAS_COMPLETED_PROFILE: []})
        result = clean_profile_completion_column(handshake_data)
        assert_column_was_renamed(self, result, StudentFields.HAS_COMPLETED_PROFILE, 'has_completed_profile')

    def test_converts_yes_and_no_to_true_and_false_and_leaves_other_values_unchanged(self):
        handshake_data = pd.DataFrame({StudentFields.HAS_COMPLETED_PROFILE: ['Yes', 'No', None]})
        expected = pd.Series([True, False, None], name='has_completed_profile')
        assert_series_equal(expected, clean_profile_completion_column(handshake_data)['has_completed_profile'])


class TestConvertAuthIDToJHED(unittest.TestCase):

    def test_renames_auth_id_column(self):
        handshake_data = pd.DataFrame({StudentFields.AUTH_ID: []})
        result = convert_auth_id_to_jhed(handshake_data)
        assert_column_was_renamed(self, result, StudentFields.AUTH_ID, 'jhed')

    def test_extracts_jhed_from_beginning_of_auth_id(self):
        handshake_data = pd.DataFrame({StudentFields.AUTH_ID: ['ajhed123@johnshopkins.edu']})
        expected = pd.Series(['ajhed123'], name='jhed')
        assert_series_equal(expected, convert_auth_id_to_jhed(handshake_data)['jhed'])

    def test_leaves_auth_id_unchanged_if_jhed_cannot_be_extracted(self):
        handshake_data = pd.DataFrame({StudentFields.AUTH_ID: ['ajhed123', None]})
        expected = pd.Series(['ajhed123', None], name='jhed')
        assert_series_equal(expected, convert_auth_id_to_jhed(handshake_data)['jhed'])


class TestAddIsPreMedColumn(unittest.TestCase):

    def test_student_is_not_pre_med_if_student_does_not_have_the_pre_health_label(self):
        handshake_data = pd.DataFrame({StudentFields.LABELS: ['']})
        expected = pd.DataFrame({StudentFields.LABELS: [''], 'is_pre_med': [False]})
        assert_frame_equal(expected, add_pre_med_column(handshake_data))

    def test_student_is_pre_med_if_student_has_the_pre_health_label(self):
        handshake_data = pd.DataFrame({StudentFields.LABELS: ['system gen: hwd, hwd: pre-health']})
        expected = pd.DataFrame({StudentFields.LABELS: ['system gen: hwd, hwd: pre-health'], 'is_pre_med': [True]})
        assert_frame_equal(expected, add_pre_med_column(handshake_data))


class TestRenameHandshakeIDColumn(unittest.TestCase):

    def test_renames_handshake_id_field(self):
        handshake_data = pd.DataFrame({StudentFields.ID: []})
        result = rename_handshake_id_column(handshake_data)
        assert_column_was_renamed(self, result, StudentFields.ID, 'handshake_id')


class TestTransformHandshakeData(unittest.TestCase):

    def test_runs_all_handshake_data_cleaning_routines_and_drops_superfluous_columns(self):
        handshake_data = pd.DataFrame({
            StudentFields.HAS_LOGGED_IN: ['Yes', 'No'],
            StudentFields.ID: ['1104932', '820934'],
            StudentFields.LABELS: ['system gen: bsph', 'hwd: pre-health'],
            StudentFields.AUTH_ID: ['jsmit2@johnshopkins.edu', 'ajohns4@johnshopkins.edu'],
            StudentFields.HAS_COMPLETED_PROFILE: ['No', 'Yes'],
            StudentFields.USERNAME: ['fur567', 'ijf383'],
            'extra_field1': ['value1', 'value2'],
        })

        expected = pd.DataFrame({
            'jhed': ['jsmit2', 'ajohns4'],
            'handshake_username': ['FUR567', 'IJF383'],
            'handshake_id': ['1104932', '820934'],
            'has_activated_handshake': [True, False],
            'has_completed_profile': [False, True],
            'is_pre_med': [False, True],
        })

        assert_frame_equal(expected, transform_handshake_data(handshake_data))


def assert_column_was_renamed(test_case, df, old_name, new_name):
    columns = df.columns
    test_case.assertTrue(old_name not in columns)
    test_case.assertTrue(new_name in columns)
