from typing import List

from src.data_model import Departments, EngagementRecord
from src.satisfaction_survey_etl.extractor import extract_survey_data
from src.satisfaction_survey_etl.transformer import transform_survey_data


def run_survey_etl(event_data: List[EngagementRecord]) -> List[dict]:
    dept_conversion_dict = {
        'Academy-Focused Office Hours': '',
        'AMS, FM, and Data Science': Departments.AMS_FM_DATA_SCI.value.name,
        'Biological and Brain Sciences': Departments.BIO_BRAIN_SCI.value.name,
        'Biomedical Engineering': Departments.BME.value.name,
        'ChemBE and Materials Science Engineering': Departments.CHEMBE_MAT_SCI.value.name,
        'Computer Science, Computer Engineering, and Electrical Engineering': Departments.COMP_ELEC_ENG.value.name,
        'Engineering Masters Students': Departments.ENG_MASTERS.value.name,
        'Humanities: History, Philosophy, and Humanistic Thought': Departments.HIST_PHIL_HUM.value.name,
        'Humanities: Language, Literatures, Film and Media': Departments.LIT_LANG_FILM.value.name,
        'Misc. Engineering': Departments.MISC_ENG.name,
        'Peer Advisor Drop-Ins': Departments.PA_DROP_INS.value.name,
        'Physical and Environmental Sciences': Departments.PHYS_ENV_SCI.value.name,
        'Pre-Health and Public Health Studies': Departments.PRE_PUB_HEALTH.value.name,
        'SOAR: Athletics': Departments.SOAR_ATHLETICS.value.name,
        'SOAR: First Year Experience (KSAS)': Departments.SOAR_FYE_KSAS.value.name,
        'SOAR: First Year Experience (WSE)': Departments.SOAR_FYE_WSE.value.name,
        'SOAR: Student Leadership and Involvement': Departments.SOAR_SLI.value.name,
        'Social Sciences: International Studies, Sociology, and Anthropology': Departments.INT_SOC_ANTH.value.name,
        'Social Sciences: Political Science, Economics, and Finance': Departments.POL_ECON_FIN.value.name,
    }
    responses = transform_survey_data(extract_survey_data(), event_data, dept_conversion_dict)
    return [response.to_dict() for response in responses]
