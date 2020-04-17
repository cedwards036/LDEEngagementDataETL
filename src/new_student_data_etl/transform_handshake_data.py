import pandas as pd

from src.handshake_fields import StudentFields


def transform_handshake_data(handshake_data: pd.DataFrame) -> pd.DataFrame:
    handshake_data = rename_handshake_id_column(handshake_data)
    handshake_data = clean_logged_in_column(handshake_data)
    handshake_data = clean_profile_completion_column(handshake_data)
    handshake_data = convert_auth_id_to_jhed(handshake_data)
    handshake_data = add_pre_med_column(handshake_data)
    handshake_data = handshake_data[[
        'jhed',
        'handshake_id',
        'has_activated_handshake',
        'has_completed_profile',
        'is_pre_med'
    ]]
    return handshake_data


def rename_handshake_id_column(handshake_data: pd.DataFrame) -> pd.DataFrame:
    return handshake_data.rename(columns={StudentFields.ID: 'handshake_id'})


def clean_logged_in_column(handshake_data: pd.DataFrame) -> pd.DataFrame:
    handshake_data = handshake_data.rename(columns={
        StudentFields.HAS_LOGGED_IN: 'has_activated_handshake'
    })
    return convert_yes_no_column_to_bool(handshake_data, 'has_activated_handshake')


def clean_profile_completion_column(handshake_data: pd.DataFrame) -> pd.DataFrame:
    handshake_data = handshake_data.rename(columns={
        StudentFields.HAS_COMPLETED_PROFILE: 'has_completed_profile'
    })
    return convert_yes_no_column_to_bool(handshake_data, 'has_completed_profile')


def convert_yes_no_column_to_bool(df: pd.DataFrame, column: str) -> pd.DataFrame:
    df[column] = df[column].replace({'Yes': True, 'No': False})
    return df


def convert_auth_id_to_jhed(handshake_data: pd.DataFrame) -> pd.DataFrame:
    handshake_data = handshake_data.rename(columns={
        StudentFields.AUTH_ID: 'jhed'
    })
    handshake_data['jhed'] = handshake_data['jhed'].apply(lambda auth_id: auth_id[:auth_id.find('@')])
    return handshake_data


def add_pre_med_column(handshake_data: pd.DataFrame) -> pd.DataFrame:
    handshake_data['is_pre_med'] = handshake_data[StudentFields.LABELS].str.contains('hwd: pre-health')
    return handshake_data
