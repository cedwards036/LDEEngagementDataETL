import unittest
from datetime import datetime

from lde_etl.engagement_data_etl.events import transform_events_data
from lde_etl.handshake_fields import EventFields


class TestEventsTransformation(unittest.TestCase):

    def test_transform_single_event_data_record(self):
        test_data = [
            {
                EventFields.ID: "340134",
                EventFields.START_DATE_TIME: "2019-09-12 13:00:00",
                EventFields.NAME: "Homewood: McKinsey Day Informational Chats",
                EventFields.STUDENT_ID: "2674069",
                EventFields.IS_PRE_REGISTERED: "Yes"
            }
        ]

        test_label_data = [
            {
                EventFields.ID: "340134",
                EventFields.LABEL: None
            }
        ]

        expected = {
            'unique_engagement_id': 'event_340134_2674069',
            'academic_year': 2020,
            'semester': 'fall2019',
            'engagement_type': 'event',
            'handshake_engagement_id': '340134',
            'start_date_time': datetime(2019, 9, 12, 13, 0, 0),
            'medium': 'in_person',
            'engagement_name': 'Homewood: McKinsey Day Informational Chats (2019-09-12 13:00:00)',
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
                EventFields.ID: "340134",
                EventFields.START_DATE_TIME: "2019-09-12 13:00:00",
                EventFields.NAME: "Homewood: McKinsey Day Informational Chats",
                EventFields.STUDENT_ID: "2674069",
                EventFields.IS_PRE_REGISTERED: "Yes"
            },
            {
                EventFields.ID: "829853",
                EventFields.START_DATE_TIME: "2019-09-01 09:30:00",
                EventFields.NAME: "Homewood: BME Event",
                EventFields.STUDENT_ID: "2980985",
                EventFields.IS_PRE_REGISTERED: "No"
            },
            {
                EventFields.ID: "1739573",
                EventFields.START_DATE_TIME: "2019-09-05 15:00:00",
                EventFields.NAME: "Homewood: ChemBE and SOAR SLI Co-Event",
                EventFields.STUDENT_ID: "233345",
                EventFields.IS_PRE_REGISTERED: "Yes"
            },
        ]

        test_label_data = [
            {
                EventFields.ID: "340134",
                EventFields.LABEL: None
            },
            {
                EventFields.ID: "829853",
                EventFields.LABEL: "hwd: bme dept"
            },
            {
                EventFields.ID: "829853",
                EventFields.LABEL: "hwd: some other label"
            },
            {
                EventFields.ID: "1739573",
                EventFields.LABEL: "hwd: soar sli"
            },
            {
                EventFields.ID: "1739573",
                EventFields.LABEL: "hwd: chembe and mat sci dept"
            },
        ]

        expected = [
            {
                'unique_engagement_id': 'event_340134_2674069',
                'engagement_type': 'event',
                'academic_year': 2020,
                'semester': 'fall2019',
                'handshake_engagement_id': '340134',
                'start_date_time': datetime(2019, 9, 12, 13, 0, 0),
                'medium': 'in_person',
                'engagement_name': 'Homewood: McKinsey Day Informational Chats (2019-09-12 13:00:00)',
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
                'academic_year': 2020,
                'semester': 'fall2019',
                'start_date_time': datetime(2019, 9, 1, 9, 30, 0),
                'medium': 'in_person',
                'engagement_name': 'Homewood: BME Event (2019-09-01 09:30:00)',
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
                'academic_year': 2020,
                'semester': 'fall2019',
                'start_date_time': datetime(2019, 9, 5, 15, 0, 0),
                'medium': 'in_person',
                'engagement_name': 'Homewood: ChemBE and SOAR SLI Co-Event (2019-09-05 15:00:00)',
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
                'academic_year': 2020,
                'semester': 'fall2019',
                'start_date_time': datetime(2019, 9, 5, 15, 0, 0),
                'medium': 'in_person',
                'engagement_name': 'Homewood: ChemBE and SOAR SLI Co-Event (2019-09-05 15:00:00)',
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
                EventFields.ID: "340134",
                EventFields.START_DATE_TIME: "2019-09-12 13:00:00",
                EventFields.NAME: "Homewood: McKinsey Day Informational Chats",
                EventFields.STUDENT_ID: "2674069",
                EventFields.IS_PRE_REGISTERED: "Yes"
            }
        ]

        test_label_data = [
            {
                EventFields.ID: "340134",
                EventFields.LABEL: "some other label"
            }
        ]

        expected = {
            'unique_engagement_id': 'event_340134_2674069',
            'engagement_type': 'event',
            'handshake_engagement_id': '340134',
            'academic_year': 2020,
            'semester': 'fall2019',
            'start_date_time': datetime(2019, 9, 12, 13, 0, 0),
            'medium': 'in_person',
            'engagement_name': 'Homewood: McKinsey Day Informational Chats (2019-09-12 13:00:00)',
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
                EventFields.ID: "829853",
                EventFields.START_DATE_TIME: "2019-09-01 09:30:00",
                EventFields.NAME: "Homewood: BME Event",
                EventFields.STUDENT_ID: "2980985",
                EventFields.IS_PRE_REGISTERED: "No"
            },
        ]

        test_label_data = [
            {
                EventFields.ID: "829853",
                EventFields.LABEL: "hwd: some other label"
            },
            {
                EventFields.ID: "829853",
                EventFields.LABEL: None
            },
            {
                EventFields.ID: "829853",
                EventFields.LABEL: "hwd: bme dept"
            },
            {
                EventFields.ID: "829853",
                EventFields.LABEL: "hwd: yet another label"
            },
            {
                EventFields.ID: "829853",
                EventFields.LABEL: "hwd: stem & innovation academy"
            },
            {
                EventFields.ID: "829853",
                EventFields.LABEL: "hwd: a third label"
            },
        ]

        expected = [
            {
                'unique_engagement_id': 'event_829853_2980985',
                'engagement_type': 'event',
                'handshake_engagement_id': '829853',
                'academic_year': 2020,
                'semester': 'fall2019',
                'start_date_time': datetime(2019, 9, 1, 9, 30, 0),
                'medium': 'in_person',
                'engagement_name': 'Homewood: BME Event (2019-09-01 09:30:00)',
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
                'academic_year': 2020,
                'semester': 'fall2019',
                'start_date_time': datetime(2019, 9, 1, 9, 30, 0),
                'medium': 'in_person',
                'engagement_name': 'Homewood: BME Event (2019-09-01 09:30:00)',
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
