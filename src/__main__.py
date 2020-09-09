from src.engagement_data_etl.run_etl import run_engagement_etl
from src.new_student_data_etl.run_etl import run_student_etl

if __name__ == '__main__':
    run_engagement_etl()
    run_student_etl()
