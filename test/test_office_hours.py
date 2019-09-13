import unittest
from datetime import datetime

from src.office_hours import transform_office_hours_data


class TestOfficeHourDataTransformation(unittest.TestCase):

    def test_data_transformation_on_ldl_office_hour(self):
        test_data = [
            {
                "appointments.id": "4298790",
                "appointments.start_date_time": "2019-09-05 11:57:51",
                "appointment_medium_on_appointments.name": "In-Person",
                "appointment_type_on_appointments.name": "Homewood: Social Sciences: Political Science, Economics, and Finance",
                "staff_member_on_appointments.email_address": "cbillin4@jhu.edu",
                "student_on_appointments.id": "4218008",
                "student_school_year_on_appointments.name": "Junior",
                "appointments.walkin": "Yes"
            }
        ]

        expected = {
            'unique_engagement_id': 'office_hours_4298790_4218008',
            'engagement_type': 'office_hours',
            'handshake_engagement_id': '4298790',
            'start_date_time': datetime(2019, 9, 5, 11, 57, 51),
            'medium': 'in_person',
            'engagement_name': 'Homewood: Social Sciences: Political Science, Economics, and Finance',
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
                'appointments.id': '4146716',
                'appointments.start_date_time': '2019-08-19 10:00:00',
                'appointment_medium_on_appointments.name': 'Virtual Appointment (Coach will Contact You)',
                'appointment_type_on_appointments.name': 'Homewood: Pre-Med',
                'staff_member_on_appointments.email_address': 'kelli.johnson@jhu.edu',
                'student_on_appointments.id': '14140603',
                'student_school_year_on_appointments.name': 'Alumni',
                'appointments.walkin': 'No'
            }
        ]

        expected = {
            'unique_engagement_id': 'office_hours_4146716_14140603',
            'engagement_type': 'office_hours',
            'handshake_engagement_id': '4146716',
            'start_date_time': datetime(2019, 8, 19, 10, 0, 0),
            'medium': 'virtual',
            'engagement_name': 'Homewood: Pre-Med',
            'engagement_category': 'pre_prof',
            'engagement_department': 'pre_prof',
            'student_handshake_id': '14140603',
            'student_school_year_at_time_of_engagement': 'Alumni',
            'student_pre_registered': True,
            'associated_staff_email': 'kelli.johnson@jhu.edu'
        }

        self.assertEqual(expected, transform_office_hours_data(test_data)[0].data)
