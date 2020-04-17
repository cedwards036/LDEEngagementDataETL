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


class InterviewFields:
    ID = 'Interview Schedules ID'
    DATE_TIME = 'Interview Schedule Checkins Checked In At Time'
    EMPLOYER = 'Employer Name'
    STUDENT_ID = 'Students (Checked In) ID'
    DATE_LIST = 'Interview Schedule Dates Date List'


class StudentFields:
    ID = 'Students ID'
    EMAIL = 'Students Email'
    USERNAME = 'Students Username'
    FIRST_NAME = 'Students First Name'
    PREF_NAME = 'Students Preferred Name'
    LAST_NAME = 'Students Last Name'
    MAJOR = 'Majors Name'
    SCHOOL_YEAR = 'School Year Name'
    AUTH_ID = 'Students Auth Identifier'
    HAS_LOGGED_IN = 'Students Has Logged In? (Yes / No)'
    HAS_COMPLETED_PROFILE = 'Profile Completion Profile Completed? (Yes / No)'
    LABELS = 'Institution Labels Name List'
