import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from src.new_student_data_etl.transform_engagement_data import count_engagements_by_type


class TestCountEngagementsByType(unittest.TestCase):

    def test_groups_engagement_data_by_handshake_id_and_counts_engagements_by_type(self):
        engagements = pd.DataFrame({
            'student_handshake_id': ['8029382', '8029382', '8029382', '8029382', '4738743'],
            'engagement_type': ['office_hours', 'event', 'event', 'interview', 'vmock'],
            'unique_engagement_id': ['1a4f32r', '028j9g4h3', 'f09j09g43', '0f902fj83', 'dd8dj9g8g'],
            'extra_field': ['', '', '', '', '']
        })
        expected = pd.DataFrame({
            'student_handshake_id': ['4738743', '8029382'],
            'event_engagements': [0, 2],
            'interview_engagements': [0, 1],
            'office_hours_engagements': [0, 1],
            'vmock_engagements': [1, 0],
            'total_engagements': [1, 4]
        })

        assert_frame_equal(expected, count_engagements_by_type(engagements))