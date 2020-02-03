import pandas as pd


def create_dataframe(data: dict, column_name: str):
    s = pd.Series(
        list(data.values()),
        index=list(data.keys()),
        name=column_name
    )
    return s.to_frame()
