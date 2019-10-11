import unittest

from src.satisfaction_survey_etl.survey_response import SurveyResponse
from src.satisfaction_survey_etl.transformer import transform_survey_data


class TestSurveyExtractor(unittest.TestCase):
    test_data = [
        ['9/4/2019 14:40:04', '10', 'Yes', '', 'It was great!', 'Biological and Brain Sciences'],
        ['9/4/2019 14:40:14', '10', 'Yes', '', '', 'Biological and Brain Sciences'],
        ['9/4/2019 18:51:40', '5', 'No', 'Everything was written in the book already', '',
         'Humanities: Social Sciences: Political Science, Economics, and Finance', '306310'],
        ['9/4/2019 18:51:42', '10', 'Yes', '', '', '', '306310']
    ]

    def test_transform_incomplete_row(self):
        test_data = [
            ['9/4/2019 14:40:04', '10', 'Yes', '', 'It was great!']
        ]
        expected = [SurveyResponse(
            nps=10,
            experience_advanced_development=True
        )]
        self.assertEqual(expected, transform_survey_data(test_data))

    def test_transform_one_office_hour_row(self):
        test_data = [
            ['9/4/2019 14:40:04', '10', 'Yes', '', 'It was great!', 'Biological and Brain Sciences']
        ]
        expected = [SurveyResponse(
            nps=10,
            experience_advanced_development=True,
            office_hour_department='Biological and Brain Sciences',
        )]
        self.assertEqual(expected, transform_survey_data(test_data))

    def test_transform_one_event_row(self):
        test_data = [
            ['9/4/2019 18:51:42', '7', 'No', '', '', '', '306310']
        ]
        expected = [SurveyResponse(
            nps=7,
            experience_advanced_development=False,
            event_id='306310',
        )]
        print(transform_survey_data(test_data)[0].to_dict())
        self.assertEqual(expected, transform_survey_data(test_data))

    def test_transform_multiple_rows(self):
        test_data = [
            ['9/4/2019 14:40:04', '10', 'Yes', '', 'It was great!', 'Biological and Brain Sciences'],
            ['9/4/2019 18:51:40', '5', 'No', 'Everything was written in the book already', '',
             'Humanities: Social Sciences: Political Science, Economics, and Finance', '643736'],
            ['9/4/2019 18:51:42', '7', 'Yes', '', '', '', '306310']
        ]
        expected = [
            SurveyResponse(
                nps=10,
                experience_advanced_development=True,
                office_hour_department='Biological and Brain Sciences',
            ),
            SurveyResponse(
                nps=5,
                experience_advanced_development=False,
                office_hour_department='Humanities: Social Sciences: Political Science, Economics, and Finance',
                event_id='643736',
            ),
            SurveyResponse(
                nps=7,
                experience_advanced_development=True,
                event_id='306310',
            )
        ]
        print(transform_survey_data(test_data)[0].to_dict())
        self.assertEqual(expected, transform_survey_data(test_data))
