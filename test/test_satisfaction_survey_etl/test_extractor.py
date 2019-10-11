import unittest

from src.satisfaction_survey_etl.extractor import extract_survey_data


class TestSurveyExtractor(unittest.TestCase):

    def test_extractor_pulls_data_of_the_correct_shape(self):
        actual = extract_survey_data()
        self.assertTrue(len(actual) > 0)
        self.assertTrue(type(actual[0]) == list)
        self.assertTrue(len(actual[0]) > 5)
        self.assertTrue(len(actual[0]) < 8)
