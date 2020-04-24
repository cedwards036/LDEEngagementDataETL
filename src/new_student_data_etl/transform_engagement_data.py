import pandas as pd
import numpy as np

def count_engagements_by_type(engagements: pd.DataFrame) -> pd.DataFrame:

    def groupby_handshake_id_and_engagement_type(df: pd.DataFrame) -> pd.DataFrame:
        grouped_df = df.groupby(['student_handshake_id', 'engagement_type'])['unique_engagement_id'].count().reset_index()
        grouped_df['engagement_type'] = grouped_df['engagement_type'] + '_engagements'
        return grouped_df

    def pivot_engagement_types(df):
        pivoted_df = df.pivot(index='student_handshake_id', columns='engagement_type', values='unique_engagement_id').fillna(0).reset_index()
        pivoted_df.axes[1].name = None
        # convert engagement count columns to ints. They might have been floats if any counts were null
        pivoted_df.iloc[:, 1:] = pivoted_df.iloc[:, 1:].astype(np.int64)
        pivoted_df['total_engagements'] = pivoted_df.iloc[:, 1:].sum(axis=1)
        return pivoted_df

    grouped_engagements = groupby_handshake_id_and_engagement_type(engagements)
    return pivot_engagement_types(grouped_engagements)