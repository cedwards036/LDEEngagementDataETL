from typing import List

from src.student_data_etl.extractors import extract_athlete_data, extract_major_data
from src.student_data_etl.output_formatters import format_student_records_for_roster_file, format_student_records_for_data_file
from src.student_data_etl.transformers import enrich_with_education_records, enrich_with_athlete_status


def _create_student_output_etl_function(formatter: callable) -> callable:
    """
    Create a function that runs the student data file ETL process and applies a
    formatter function to the result.

    :param formatter: the formatter function to apply to the student data
    :return: a formatted dataset, ready for outputting to a file
    """

    def run_etl(handshake_data: List[dict], major_data_filepath: str, athlete_filepath: str) -> List[dict]:
        major_data = extract_major_data(major_data_filepath)
        athlete_data = extract_athlete_data(athlete_filepath)
        return formatter(
            enrich_with_athlete_status(
                enrich_with_education_records(
                    handshake_data, major_data
                ),
                athlete_data
            )
        )

    return run_etl


run_roster_file_etl = _create_student_output_etl_function(format_student_records_for_roster_file)
run_data_file_etl = _create_student_output_etl_function(format_student_records_for_data_file)
