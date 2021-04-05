from lde_etl.engagement_data_etl.run_etl import run_engagement_etl
from lde_etl.student_data_etl.run_etl import run_student_etl
from lde_etl.common import load_config
import getpass
import os

if __name__ == '__main__':
    jhed = input('Please input your JHED: ').strip()
    config = load_config(f'{os.path.dirname(os.path.abspath(__file__))}/../config.json', jhed)
    config['handshake_email'] = input('Please input your Handshake email address: ').strip()
    config['handshake_pw'] = getpass.getpass('Please input your Handshake password: ').strip()
    run_engagement_etl(config)
    run_student_etl(config)
