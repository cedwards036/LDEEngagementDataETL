from datetime import datetime
from enum import Enum


class Categories(Enum):
    """The possible engagement category values"""
    LDL_DEPARTMENT = 'ldl_department'
    LDL_NO_DEPARTMENT = 'ldl_no_department'
    LDL_ACADEMY = 'ldl_academy'
    PRE_PROF = 'pre_prof'
    ENG_MASTERS = 'eng_masters'
    AMS_FM_DATA_SCI = 'ams_fm_data_sci'
    SOAR = 'soar'
    PA_DROP_INS = 'pa_drop_ins'


class Department:
    """A department grouping"""

    def __init__(self, name: str, category: Categories):
        self._name = name
        self._category = category

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category.value


class Departments(Enum):
    """The possible engagement department values"""
    AMS_FM_DATA_SCI = Department('ams_fm_data_sci', Categories.AMS_FM_DATA_SCI)
    AMS_UGRAD = Department('ams_ugrad', Categories.LDL_DEPARTMENT)
    BIO_SCI = Department('bio_sci', Categories.LDL_DEPARTMENT)  # archived
    BIO_BRAIN_SCI = Department('bio_brain_sci', Categories.LDL_DEPARTMENT)  # archived
    BME = Department('bme', Categories.LDL_DEPARTMENT)
    BRAIN_SCI = Department('brain_sci', Categories.LDL_DEPARTMENT)
    CHEMBE = Department('chembe', Categories.LDL_DEPARTMENT)
    CHEMBE_MAT_SCI = Department('chembe_mat_sci', Categories.LDL_DEPARTMENT) # archived
    CIVIL_ENG = Department('civil_eng', Categories.LDL_DEPARTMENT)
    COMP_ELEC_ENG = Department('comp_elec_eng', Categories.LDL_DEPARTMENT)
    ENG_MASTERS = Department('eng_masters', Categories.ENG_MASTERS)
    ENV_ENG = Department('env_eng', Categories.LDL_DEPARTMENT)
    HIST_PHIL_HUM = Department('hist_phil_hum', Categories.LDL_DEPARTMENT)  # archived
    HISTORY = Department('history', Categories.LDL_DEPARTMENT)  # archived
    HUMANITIES = Department('humanities', Categories.LDL_DEPARTMENT)
    INT_SOC_ANTH = Department('int_soc_anth', Categories.LDL_DEPARTMENT)  # archived
    LIT_LANG_FILM = Department('lit_lang_film', Categories.LDL_DEPARTMENT)  # archived
    MAT_SCI = Department('mat_sci', Categories.LDL_DEPARTMENT)
    MECH_ENG = Department('mech_eng', Categories.LDL_DEPARTMENT)
    MISC_ENG = Department('misc_eng', Categories.LDL_DEPARTMENT)  # archived
    PA_DROP_INS = Department('pa_drop_ins', Categories.PA_DROP_INS)
    PHYS_ENV_SCI = Department('phys_env_sci', Categories.LDL_DEPARTMENT)  # archived
    POL_ECON_FIN = Department('pol_econ_fin', Categories.LDL_DEPARTMENT)  # archived
    PRE_PUB_HEALTH = Department('pre_pub_health', Categories.LDL_DEPARTMENT)
    SCIENCES = Department('sciences', Categories.LDL_DEPARTMENT)
    SOAR_ATHLETICS = Department('soar_athletics', Categories.SOAR)
    SOAR_CSS = Department('soar_css', Categories.SOAR)
    SOAR_DIV_INCL = Department('soar_div_incl', Categories.LDL_DEPARTMENT)
    SOAR_FYE_KSAS = Department('soar_fye_ksas', Categories.SOAR)
    SOAR_FYE_WSE = Department('soar_fye_wse', Categories.SOAR)
    SOAR_SLI = Department('soar_sli', Categories.SOAR)
    SOCIAL_SCI = Department('social_sci', Categories.LDL_DEPARTMENT)
    STEM_ACADEMY = Department('stem_academy', Categories.LDL_ACADEMY)
    AMM_ACADEMY = Department('amm_academy', Categories.LDL_ACADEMY)
    FINANCE_ACADEMY = Department('finance_academy', Categories.LDL_ACADEMY)
    CONSUTING_ACADEMY = Department('consulting_academy', Categories.LDL_ACADEMY)
    HEALTH_SCI_ACADEMY = Department('health_sci_academy', Categories.LDL_ACADEMY)
    NP_GOV_ACADEMY = Department('np_gov_academy', Categories.LDL_ACADEMY)
    PRE_PROF = Department('pre_prof', Categories.PRE_PROF)
    NO_DEPARTMENT = Department('no_dept', Categories.LDL_NO_DEPARTMENT)
    EP = Department('wse_ep', Categories.LDL_DEPARTMENT)
    WGS = Department('wgs', Categories.LDL_DEPARTMENT)
    OPERATIONS = Department('operations', Categories.LDL_DEPARTMENT)


class EngagementTypes(Enum):
    """The possible engagement type values"""
    OFFICE_HOURS = 'office_hours'
    EVENT = 'event'
    CAREER_FAIR = 'career_fair'
    INTERVIEW = 'interview'


class Mediums(Enum):
    """The possible medium values"""
    IN_PERSON = 'in_person'
    VIRTUAL = 'virtual'
    EMAIL = 'email'


class EngagementRecord:
    """A data record representing a single student engagement"""

    def __init__(self, engagement_type: EngagementTypes, handshake_engagement_id: str,
                 start_date_time: datetime, medium: Mediums, engagement_name: str,
                 engagement_department: Department, student_handshake_id: str,
                 student_school_year_at_time_of_engagement: str,
                 student_pre_registered: bool, associated_staff_email: str):
        self.data = {
            'unique_engagement_id': self._unique_engagement_id(engagement_type,
                                                               handshake_engagement_id,
                                                               student_handshake_id),
            'handshake_engagement_id': handshake_engagement_id,
            'engagement_type': engagement_type.value,
            'academic_year': self.academic_year(start_date_time),
            'semester': self._semester(start_date_time),
            'start_date_time': start_date_time,
            'medium': medium.value,
            'engagement_name': engagement_name,
            'engagement_category': engagement_department.category,
            'engagement_department': engagement_department.name,
            'student_handshake_id': student_handshake_id,
            'student_school_year_at_time_of_engagement': student_school_year_at_time_of_engagement,
            'student_pre_registered': student_pre_registered,
            'associated_staff_email': associated_staff_email
        }

    def _unique_engagement_id(self, engagement_type: EngagementTypes, handshake_engagement_id: str,
                              student_handshake_id: str):
        return f'{engagement_type.value}_{handshake_engagement_id}_{student_handshake_id}'

    @staticmethod
    def academic_year(date):
        if date.month < 6:
            return date.year
        else:
            return date.year + 1

    @staticmethod
    def _semester(date):
        if date.month < 6:
            return f'spring{date.year}'
        elif date.month < 9:
            return f'summer{date.year}'
        else:
            return f'fall{date.year}'
