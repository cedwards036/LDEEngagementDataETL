class AppointmentFields:
    ID = 'Appointments ID'
    START_DATE_TIME = 'Appointments Start Date Time'
    MEDIUM = 'Appointment Medium Name'
    TYPE_LENGTH = 'Appointment Type Length (Minutes)'
    TYPE = 'Appointment Type Name'
    STATUS = 'Appointment Status'
    STAFF_MEMBER_EMAIL = 'Staff Member Email'
    STUDENT_USERNAME = 'Student Username'
    STUDENT_ID = 'Student ID'
    STUDENT_SCHOOL_YEAR = 'Student School Year (at Appt. Time) Name'
    STUDENT_MAJORS = 'Student Majors (at Appt. Time) Name'
    STUDENT_COLLEGE_ID = 'Student College (at Appt. Time) ID'
    STUDENT_LABELS_LIST = 'Student Institution Labels Name List'
    IS_DROP_IN = 'Appointments Drop-in? (Yes / No)'


class EventFields:
    ID = 'Events ID'
    START_DATE_TIME = 'Events Start Date Time'
    NAME = 'Events Name'
    STUDENT_ID = 'Student Attendees ID'
    IS_PRE_REGISTERED = 'Attendees Pre-Registered? (Yes / No)'
    LABEL = 'Institution Labels Name'


class CareerFairFields:
    ID = 'Career Fair ID'
    START_DATE_TIME = 'Career Fair Session Session Start Time'
    NAME = 'Career Fair Name'
    STUDENT_ID = 'Student Attendees ID'
    IS_PRE_REGISTERED = 'Career Fair Session Attendees Pre-Registered? (Yes / No)'
