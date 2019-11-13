import unittest
from datetime import datetime

from src.engagement_data_etl.office_hours import transform_office_hours_data
from src.handshake_fields import AppointmentFields


class TestOfficeHourDataTransformation(unittest.TestCase):

    def test_data_transformation_on_ldl_office_hour(self):
        test_data = [
            {
                AppointmentFields.ID: "4298790",
                AppointmentFields.START_DATE_TIME: "2019-09-05 11:57:51",
                AppointmentFields.MEDIUM: "In-Person",
                AppointmentFields.TYPE: "Homewood: Social Sciences: Political Science, Economics, and Finance",
                AppointmentFields.STAFF_MEMBER_EMAIL: "cbillin4@jhu.edu",
                AppointmentFields.STUDENT_ID: "4218008",
                AppointmentFields.STUDENT_SCHOOL_YEAR: "Junior",
                AppointmentFields.IS_DROP_IN: "Yes"
            }
        ]

        expected = {
            'unique_engagement_id': 'office_hours_4298790_4218008',
            'engagement_type': 'office_hours',
            'handshake_engagement_id': '4298790',
            'start_date_time': datetime(2019, 9, 5, 11, 57, 51),
            'medium': 'in_person',
            'engagement_name': 'Homewood: Social Sciences: Political Science, Economics, and Finance Office Hours',
            'engagement_category': 'ldl_department',
            'engagement_department': 'pol_econ_fin',
            'student_handshake_id': '4218008',
            'student_school_year_at_time_of_engagement': 'Junior',
            'student_pre_registered': False,
            'associated_staff_email': 'cbillin4@jhu.edu'
        }

        self.assertEqual(expected, transform_office_hours_data(test_data)[0].data)

    def test_data_transformation_on_pre_prof(self):
        test_data = [
            {
                AppointmentFields.ID: '4146716',
                AppointmentFields.START_DATE_TIME: '2019-08-19 10:00:00',
                AppointmentFields.MEDIUM: 'Virtual Appointment (Coach will Contact You)',
                AppointmentFields.TYPE: 'Homewood: Pre-Med',
                AppointmentFields.STAFF_MEMBER_EMAIL: 'kelli.johnson@jhu.edu',
                AppointmentFields.STUDENT_ID: '14140603',
                AppointmentFields.STUDENT_SCHOOL_YEAR: 'Alumni',
                AppointmentFields.IS_DROP_IN: 'No'
            }
        ]

        expected = {
            'unique_engagement_id': 'office_hours_4146716_14140603',
            'engagement_type': 'office_hours',
            'handshake_engagement_id': '4146716',
            'start_date_time': datetime(2019, 8, 19, 10, 0, 0),
            'medium': 'virtual',
            'engagement_name': 'Homewood: Pre-Med Appointment',
            'engagement_category': 'pre_prof',
            'engagement_department': 'pre_prof',
            'student_handshake_id': '14140603',
            'student_school_year_at_time_of_engagement': 'Alumni',
            'student_pre_registered': True,
            'associated_staff_email': 'kelli.johnson@jhu.edu'
        }

        self.assertEqual(expected, transform_office_hours_data(test_data)[0].data)
