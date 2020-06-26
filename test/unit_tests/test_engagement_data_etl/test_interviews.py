import unittest
from datetime import datetime

from src.engagement_data_etl.interviews import transform_interviews_data, format_list
from src.handshake_fields import InterviewFields


class TestInterviewsTransformation(unittest.TestCase):

    def test_transform_interview_engagement(self):
        test_data = [
            {
                InterviewFields.ID: "289843",
                InterviewFields.DATE_TIME: "2019-10-08 13:00:00",
                InterviewFields.EMPLOYER: "Deloitte",
                InterviewFields.STUDENT_ID: "937574353",
                InterviewFields.DATE_LIST: "2019-10-08"
            }
        ]

        expected = {
            'unique_engagement_id': 'interview_289843_937574353',
            'engagement_type': 'interview',
            'handshake_engagement_id': '289843',
            'academic_year': 2020,
            'semester': 'fall2019',
            'start_date_time': datetime(2019, 10, 8, 13, 0, 0),
            'medium': 'in_person',
            'engagement_name': 'Deloitte Interviews on 2019-10-08',
            'engagement_category': 'ldl_no_department',
            'engagement_department': 'no_dept',
            'student_handshake_id': '937574353',
            'student_school_year_at_time_of_engagement': None,
            'student_pre_registered': True,
            'associated_staff_email': None
        }

        self.assertEqual(expected, transform_interviews_data(test_data)[0].data)


class TestListFormatter(unittest.TestCase):

    def test_with_single_item(self):
        self.assertEqual('a', format_list('a'))

    def test_with_two_items(self):
        self.assertEqual('a and b', format_list('a, b'))

    def test_with_three_items(self):
        self.assertEqual('a, b, and c', format_list('a, b, c'))
