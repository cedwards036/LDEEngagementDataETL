import unittest
from datetime import datetime

from src.engagement_data_etl.events import transform_events_data


class TestEventsTransformation(unittest.TestCase):

    def test_transform_single_event_data_record(self):
        test_data = [
            {
                "events.id": "340134",
                "events.start_date_time": "2019-09-12 13:00:00",
                "events.name": "Homewood: McKinsey Day Informational Chats",
                "attendee_users_on_events.id": "2674069",
                "attendees_on_events.registered": "Yes"
            }
        ]

        test_label_data = [
            {
                "events.id": "340134",
                "added_institution_labels_on_events.name": None
            }
        ]

        expected = {
            'unique_engagement_id': 'event_340134_2674069',
            'engagement_type': 'event',
            'handshake_engagement_id': '340134',
            'start_date_time': datetime(2019, 9, 12, 13, 0, 0),
            'medium': 'in_person',
            'engagement_name': 'Homewood: McKinsey Day Informational Chats',
            'engagement_category': 'ldl_no_department',
            'engagement_department': 'no_dept',
            'student_handshake_id': '2674069',
            'student_school_year_at_time_of_engagement': None,
            'student_pre_registered': True,
            'associated_staff_email': None
        }

        self.assertEqual(expected, transform_events_data(test_data, test_label_data)[0].data)

    def test_transform_multiple_event_data_records(self):
        test_data = [
            {
                "events.id": "340134",
                "events.start_date_time": "2019-09-12 13:00:00",
                "events.name": "Homewood: McKinsey Day Informational Chats",
                "attendee_users_on_events.id": "2674069",
                "attendees_on_events.registered": "Yes"
            },
            {
                "events.id": "829853",
                "events.start_date_time": "2019-09-01 09:30:00",
                "events.name": "Homewood: BME Event",
                "attendee_users_on_events.id": "2980985",
                "attendees_on_events.registered": "No"
            },
            {
                "events.id": "1739573",
                "events.start_date_time": "2019-09-05 15:00:00",
                "events.name": "Homewood: ChemBE and SOAR SLI Co-Event",
                "attendee_users_on_events.id": "233345",
                "attendees_on_events.registered": "Yes"
            },
        ]

        test_label_data = [
            {
                "events.id": "340134",
                "added_institution_labels_on_events.name": None
            },
            {
                "events.id": "829853",
                "added_institution_labels_on_events.name": "hwd: bme dept"
            },
            {
                "events.id": "829853",
                "added_institution_labels_on_events.name": "hwd: some other label"
            },
            {
                "events.id": "1739573",
                "added_institution_labels_on_events.name": "hwd: soar sli"
            },
            {
                "events.id": "1739573",
                "added_institution_labels_on_events.name": "hwd: chembe and mat sci dept"
            },
        ]

        expected = [
            {
                'unique_engagement_id': 'event_340134_2674069',
                'engagement_type': 'event',
                'handshake_engagement_id': '340134',
                'start_date_time': datetime(2019, 9, 12, 13, 0, 0),
                'medium': 'in_person',
                'engagement_name': 'Homewood: McKinsey Day Informational Chats',
                'engagement_category': 'ldl_no_department',
                'engagement_department': 'no_dept',
                'student_handshake_id': '2674069',
                'student_school_year_at_time_of_engagement': None,
                'student_pre_registered': True,
                'associated_staff_email': None
            },
            {
                'unique_engagement_id': 'event_829853_2980985',
                'engagement_type': 'event',
                'handshake_engagement_id': '829853',
                'start_date_time': datetime(2019, 9, 1, 9, 30, 0),
                'medium': 'in_person',
                'engagement_name': 'Homewood: BME Event',
                'engagement_category': 'ldl_department',
                'engagement_department': 'bme',
                'student_handshake_id': '2980985',
                'student_school_year_at_time_of_engagement': None,
                'student_pre_registered': False,
                'associated_staff_email': None
            },
            {
                'unique_engagement_id': 'event_1739573_233345',
                'engagement_type': 'event',
                'handshake_engagement_id': '1739573',
                'start_date_time': datetime(2019, 9, 5, 15, 0, 0),
                'medium': 'in_person',
                'engagement_name': 'Homewood: ChemBE and SOAR SLI Co-Event',
                'engagement_category': 'soar',
                'engagement_department': 'soar_sli',
                'student_handshake_id': '233345',
                'student_school_year_at_time_of_engagement': None,
                'student_pre_registered': True,
                'associated_staff_email': None
            },
            {
                'unique_engagement_id': 'event_1739573_233345',
                'engagement_type': 'event',
                'handshake_engagement_id': '1739573',
                'start_date_time': datetime(2019, 9, 5, 15, 0, 0),
                'medium': 'in_person',
                'engagement_name': 'Homewood: ChemBE and SOAR SLI Co-Event',
                'engagement_category': 'ldl_department',
                'engagement_department': 'chembe_mat_sci',
                'student_handshake_id': '233345',
                'student_school_year_at_time_of_engagement': None,
                'student_pre_registered': True,
                'associated_staff_email': None
            },
        ]

        actual = [record.data for record in transform_events_data(test_data, test_label_data)]
        self.assertEqual(expected, actual)

    def test_transform_non_dept_labeled_event(self):
        test_data = [
            {
                "events.id": "340134",
                "events.start_date_time": "2019-09-12 13:00:00",
                "events.name": "Homewood: McKinsey Day Informational Chats",
                "attendee_users_on_events.id": "2674069",
                "attendees_on_events.registered": "Yes"
            }
        ]

        test_label_data = [
            {
                "events.id": "340134",
                "added_institution_labels_on_events.name": "some other label"
            }
        ]

        expected = {
            'unique_engagement_id': 'event_340134_2674069',
            'engagement_type': 'event',
            'handshake_engagement_id': '340134',
            'start_date_time': datetime(2019, 9, 12, 13, 0, 0),
            'medium': 'in_person',
            'engagement_name': 'Homewood: McKinsey Day Informational Chats',
            'engagement_category': 'ldl_no_department',
            'engagement_department': 'no_dept',
            'student_handshake_id': '2674069',
            'student_school_year_at_time_of_engagement': None,
            'student_pre_registered': True,
            'associated_staff_email': None
        }

        self.assertEqual(expected, transform_events_data(test_data, test_label_data)[0].data)

    def test_transform_no_dept_label_before_dept_label(self):
        test_data = [
            {
                "events.id": "829853",
                "events.start_date_time": "2019-09-01 09:30:00",
                "events.name": "Homewood: BME Event",
                "attendee_users_on_events.id": "2980985",
                "attendees_on_events.registered": "No"
            },
        ]

        test_label_data = [
            {
                "events.id": "829853",
                "added_institution_labels_on_events.name": "hwd: some other label"
            },
            {
                "events.id": "829853",
                "added_institution_labels_on_events.name": None
            },
            {
                "events.id": "829853",
                "added_institution_labels_on_events.name": "hwd: bme dept"
            },
            {
                "events.id": "829853",
                "added_institution_labels_on_events.name": "hwd: yet another label"
            },
            {
                "events.id": "829853",
                "added_institution_labels_on_events.name": "hwd: stem & innovation academy"
            },
            {
                "events.id": "829853",
                "added_institution_labels_on_events.name": "hwd: a third label"
            },
        ]

        expected = [
            {
                'unique_engagement_id': 'event_829853_2980985',
                'engagement_type': 'event',
                'handshake_engagement_id': '829853',
                'start_date_time': datetime(2019, 9, 1, 9, 30, 0),
                'medium': 'in_person',
                'engagement_name': 'Homewood: BME Event',
                'engagement_category': 'ldl_department',
                'engagement_department': 'bme',
                'student_handshake_id': '2980985',
                'student_school_year_at_time_of_engagement': None,
                'student_pre_registered': False,
                'associated_staff_email': None
            },
            {
                'unique_engagement_id': 'event_829853_2980985',
                'engagement_type': 'event',
                'handshake_engagement_id': '829853',
                'start_date_time': datetime(2019, 9, 1, 9, 30, 0),
                'medium': 'in_person',
                'engagement_name': 'Homewood: BME Event',
                'engagement_category': 'ldl_academy',
                'engagement_department': 'stem_academy',
                'student_handshake_id': '2980985',
                'student_school_year_at_time_of_engagement': None,
                'student_pre_registered': False,
                'associated_staff_email': None
            }
        ]

        actual = [record.data for record in transform_events_data(test_data, test_label_data)]
        self.assertEqual(expected, actual)
