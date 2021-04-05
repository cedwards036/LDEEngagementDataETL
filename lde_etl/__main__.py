from lde_etl.engagement_data_etl.run_etl import run_engagement_etl
from lde_etl.student_data_etl.run_etl import run_student_etl
from lde_etl.common import CONFIG

if __name__ == '__main__':
    run_engagement_etl(CONFIG)
    run_student_etl(CONFIG)
