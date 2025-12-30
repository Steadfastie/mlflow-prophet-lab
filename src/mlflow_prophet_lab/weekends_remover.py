import pandas as pd


def remove_weekends(df: pd.DataFrame) -> pd.DataFrame:
    """Remove weekends from the dataframe."""
    clean = df.copy()
    clean = clean[~df['ds'].dt.day_name().isin(['Saturday', 'Sunday'])]
    return clean