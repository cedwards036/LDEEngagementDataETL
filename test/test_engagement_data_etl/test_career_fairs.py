import unittest
from datetime import datetime

from lde_etl.engagement_data_etl.career_fairs import transform_fair_data
from lde_etl.handshake_fields import CareerFairFields


class TestCareerFairTransformation(unittest.TestCase):

    def test_transform_single_fair_data_record(self):
        test_data = [
            {
                CareerFairFields.ID: "9813",
                CareerFairFields.START_DATE_TIME: "2018-03-21 11:00:00",
                CareerFairFields.NAME: "Homewood: Johns Hopkins University Spring 2018 Career Fair",
                CareerFairFields.STUDENT_ID: "2674562",
                CareerFairFields.IS_PRE_REGISTERED: "Yes"
            },
        ]

        expected = {
            'unique_engagement_id': 'career_fair_9813_2674562',
            'engagement_type': 'career_fair',
            'handshake_engagement_id': '9813',
            'academic_year': 2018,
            'semester': 'spring2018',
            'start_date_time': datetime(2018, 3, 21, 11, 0, 0),
            'medium': 'in_person',
            'engagement_name': 'Homewood: Johns Hopkins University Spring 2018 Career Fair',
            'engagement_category': 'ldl_no_department',
            'engagement_department': 'no_dept',
            'student_handshake_id': '2674562',
            'student_school_year_at_time_of_engagement': None,
            'student_pre_registered': True,
            'associated_staff_email': None
        }

        self.assertEqual(expected, transform_fair_data(test_data)[0].data)
