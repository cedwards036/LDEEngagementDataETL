import unittest
from datetime import datetime

from src.engagement_data_etl.career_fairs import transform_fair_data


class TestCareerFairTransformation(unittest.TestCase):

    def test_transform_single_fair_data_record(self):
        test_data = [
            {
                "session_career_fair_on_career_fair_session_attendees.id": "9813",
                "career_fair_session_on_career_fair_session_attendees.start_date_time_time": "2019-09-26 11:00:00",
                "session_career_fair_on_career_fair_session_attendees.name": "Homewood: Johns Hopkins University Fall 2019 Career Fair",
                "user_on_career_fair_session_attendees.id": "2674562",
                "career_fair_session_attendees.registered": "Yes"
            },
        ]

        expected = {
            'unique_engagement_id': 'career_fair_9813_2674562',
            'engagement_type': 'career_fair',
            'handshake_engagement_id': '9813',
            'start_date_time': datetime(2019, 9, 26, 11, 0, 0),
            'medium': 'in_person',
            'engagement_name': 'Homewood: Johns Hopkins University Fall 2019 Career Fair',
            'engagement_category': 'ldl_no_department',
            'engagement_department': 'no_dept',
            'student_handshake_id': '2674562',
            'student_school_year_at_time_of_engagement': None,
            'student_pre_registered': True,
            'associated_staff_email': None
        }

        self.assertEqual(expected, transform_fair_data(test_data)[0].data)
