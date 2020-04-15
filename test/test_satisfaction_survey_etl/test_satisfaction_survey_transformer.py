import io
import sys
import unittest
from typing import List

from src.data_model import (EngagementTypes, EngagementRecord, Departments,
                            Mediums)
from src.satisfaction_survey_etl.survey_response import SurveyResponse
from src.satisfaction_survey_etl.transformer import (parse_raw_survey_data,
                                                     create_event_data_lookup,
                                                     add_event_depts_to_survey_data,
                                                     convert_office_hour_depts_in_survey_data)


def assert_survey_data_is_equal(test_obj, expected: List[SurveyResponse], actual: List[SurveyResponse]):
    expected_dicts = [response.to_dict() for response in expected]
    actual_dicts = [response.to_dict() for response in actual]
    test_obj.assertEqual(expected_dicts, actual_dicts)


class TestSurveyTransformer(unittest.TestCase):

    def test_transform_incomplete_row(self):
        test_data = [
            ['9/4/2019 14:40:04', '10', 'Yes', '', 'It was great!']
        ]
        expected = [SurveyResponse(
            response_id="1",
            nps=10,
            experience_advanced_development=True
        )]
        assert_survey_data_is_equal(self, expected, parse_raw_survey_data(test_data))

    def test_transform_one_office_hour_row(self):
        test_data = [
            ['9/4/2019 14:40:04', '10', 'Yes', '', 'It was great!', 'Biological and Brain Sciences']
        ]
        expected = [SurveyResponse(
            response_id="1",
            nps=10,
            experience_advanced_development=True,
            engagement_type=EngagementTypes.OFFICE_HOURS.value,
            office_hour_department='Biological and Brain Sciences',
        )]
        self.assertEqual(expected, parse_raw_survey_data(test_data))

    def test_transform_one_event_row(self):
        test_data = [
            ['9/4/2019 18:51:42', '7', 'No', '', '', '', '306310']
        ]
        expected = [SurveyResponse(
            response_id="1",
            nps=7,
            experience_advanced_development=False,
            engagement_type=EngagementTypes.EVENT.value,
            event_id='306310',
        )]
        self.assertEqual(expected, parse_raw_survey_data(test_data))

    def test_transform_multiple_rows(self):
        test_data = [
            ['9/4/2019 14:40:04', '10', 'Yes', '', 'It was great!', 'Biological and Brain Sciences'],
            ['9/4/2019 18:51:40', '5', 'No', 'Everything was written in the book already', '',
             'Humanities: Social Sciences: Political Science, Economics, and Finance', '643736'],
            ['9/4/2019 18:51:42', '7', 'Yes', '', '', '', '306310']
        ]
        expected = [
            SurveyResponse(
                response_id="1",
                nps=10,
                experience_advanced_development=True,
                engagement_type=EngagementTypes.OFFICE_HOURS.value,
                office_hour_department='Biological and Brain Sciences',
            ),
            SurveyResponse(
                response_id="2",
                nps=5,
                experience_advanced_development=False,
                engagement_type=EngagementTypes.EVENT.value,
                event_id='643736',
            ),
            SurveyResponse(
                response_id="3",
                nps=7,
                experience_advanced_development=True,
                engagement_type=EngagementTypes.EVENT.value,
                event_id='306310',
            )
        ]
        self.assertEqual(expected, parse_raw_survey_data(test_data))


class TestCreateEventDataLookup(unittest.TestCase):

    def test_create_event_data_lookup(self):
        test_event_data = [
            EngagementRecord(
                engagement_type=EngagementTypes.EVENT,
                handshake_engagement_id='340134',
                start_date_time=None,
                medium=Mediums.IN_PERSON,
                engagement_name='Homewood: McKinsey Day Informational Chats',
                engagement_department=Departments.NO_DEPARTMENT.value,
                student_handshake_id='2674069',
                student_school_year_at_time_of_engagement=None,
                student_pre_registered=False,
                associated_staff_email=None
            ),
            EngagementRecord(
                engagement_type=EngagementTypes.EVENT,
                handshake_engagement_id='5374545',
                start_date_time=None,
                medium=Mediums.IN_PERSON,
                engagement_name='Homewood: BME Event',
                engagement_department=Departments.BME.value,
                student_handshake_id='2674069',
                student_school_year_at_time_of_engagement=None,
                student_pre_registered=False,
                associated_staff_email=None
            ),
        ]

        expected = {
            '340134': 'no_dept',
            '5374545': 'bme'
        }

        self.assertEqual(expected, create_event_data_lookup(test_event_data))


class TestAddEventDeptsToSurveyData(unittest.TestCase):

    def test_skips_rows_with_no_event_id(self):
        test_event_data = {
            '643736': 'no_dept',
            '306310': 'bme'
        }

        test_survey_data = [
            SurveyResponse(
                nps=5,
                experience_advanced_development=False,
            ),
            SurveyResponse(
                nps=7,
                experience_advanced_development=True,
                engagement_type=EngagementTypes.OFFICE_HOURS.value,
                office_hour_department='Biological and Brain Sciences',
            )
        ]

        expected = [
            SurveyResponse(
                nps=5,
                experience_advanced_development=False,
            ),
            SurveyResponse(
                nps=7,
                experience_advanced_development=True,
                engagement_type=EngagementTypes.OFFICE_HOURS.value,
                office_hour_department='Biological and Brain Sciences',
            )
        ]

        self.assertEqual(expected, add_event_depts_to_survey_data(test_event_data, test_survey_data))

    def test_add_event_data_to_matching_survey_data(self):
        test_event_data = {
            '643736': 'no_dept',
            '306310': 'bme'
        }

        test_survey_data = [
            SurveyResponse(
                nps=5,
                experience_advanced_development=False,
                engagement_type=EngagementTypes.EVENT.value,
                event_id='643736',
            ),
            SurveyResponse(
                nps=7,
                experience_advanced_development=True,
                engagement_type=EngagementTypes.EVENT.value,
                event_id='306310',
            )
        ]

        expected = [
            SurveyResponse(
                nps=5,
                experience_advanced_development=False,
                engagement_type=EngagementTypes.EVENT.value,
                event_id='643736',
                department='no_dept'
            ),
            SurveyResponse(
                nps=7,
                experience_advanced_development=True,
                engagement_type=EngagementTypes.EVENT.value,
                event_id='306310',
                department='bme'
            )
        ]

        self.assertEqual(expected, add_event_depts_to_survey_data(test_event_data, test_survey_data))

    def test_prints_warning_when_no_event_match_is_found(self):
        captured_output = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        test_event_data = {
            '643736': 'no_dept',
        }

        test_survey_data = [
            SurveyResponse(
                nps=7,
                experience_advanced_development=True,
                engagement_type=EngagementTypes.EVENT.value,
                event_id='306310',
            )
        ]
        add_event_depts_to_survey_data(test_event_data, test_survey_data)
        sys.stdout = old_stdout
        self.assertEqual(f'WARNING: Satisfaction survey event id "306310" does not appear in Handshake data\n', captured_output.getvalue())


class TestConvertOfficeHourDeptsInSurveyData(unittest.TestCase):

    def test_skips_rows_with_no_office_hour_dept(self):
        test_survey_data = [
            SurveyResponse(
                nps=5,
                experience_advanced_development=False,
            ),
            SurveyResponse(
                nps=7,
                experience_advanced_development=True,
                engagement_type=EngagementTypes.OFFICE_HOURS.value,
                event_id='234895'
            )
        ]

        expected = [
            SurveyResponse(
                nps=5,
                experience_advanced_development=False,
            ),
            SurveyResponse(
                nps=7,
                experience_advanced_development=True,
                engagement_type=EngagementTypes.OFFICE_HOURS.value,
                event_id='234895'
            )
        ]
        self.assertEqual(expected, convert_office_hour_depts_in_survey_data(test_survey_data, {}))

    def test_converts_depts_with_defined_conversions(self):
        test_survey_data = [
            SurveyResponse(
                nps=5,
                experience_advanced_development=False,
                office_hour_department='Bio and Brain Sci'
            ),
            SurveyResponse(
                nps=7,
                experience_advanced_development=True,
                engagement_type=EngagementTypes.OFFICE_HOURS.value,
                office_hour_department='Literature, Language, and Film',
                event_id='234895'
            )
        ]

        conversion_dict = {
            'Literature, Language, and Film': 'lit_lang_film',
            'Bio and Brain Sci': 'bio_brain_sci'
        }

        expected = [
            SurveyResponse(
                nps=5,
                experience_advanced_development=False,
                office_hour_department='Bio and Brain Sci',
                department='bio_brain_sci'
            ),
            SurveyResponse(
                nps=7,
                experience_advanced_development=True,
                engagement_type=EngagementTypes.OFFICE_HOURS.value,
                office_hour_department='Literature, Language, and Film',
                event_id='234895',
                department='lit_lang_film'
            )
        ]
        self.assertEqual(expected, convert_office_hour_depts_in_survey_data(test_survey_data, conversion_dict))

    def test_throws_error_when_encountering_unknown_dept(self):
        test_survey_data = [
            SurveyResponse(
                nps=5,
                experience_advanced_development=False,
                office_hour_department='Some Other Department'
            ),
        ]

        conversion_dict = {
            'Literature, Language, and Film': 'lit_lang_film',
            'Bio and Brain Sci': 'bio_brain_sci'
        }

        with self.assertRaises(ValueError):
            convert_office_hour_depts_in_survey_data(test_survey_data, conversion_dict)
