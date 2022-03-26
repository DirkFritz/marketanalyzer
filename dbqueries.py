import pandas as pd


from db import Db
from ndxdata import NdxData


def getNdxData(start_date, symbols, symbols_single):
    db = Db()
    data_db = db.select_historic_date(start_date)
    stocks_db_df = pd.DataFrame(
        columns=["Symbol", "DateTime", "Open", "Close", "High", "Low", "Volume"]
    )
    stocks_db_df = pd.concat(
        [
            stocks_db_df,
            pd.DataFrame(
                data_db,
                columns=[
                    "Symbol",
                    "DateTime",
                    "Open",
                    "Close",
                    "High",
                    "Low",
                    "Volume",
                ],
            ),
        ]
    )

    group_name = ""
    for symbol in symbols:
        group_name = group_name + symbol[0]

    ndx_data = NdxData("gs://lt-capital.de/nasdaq_screener_2.csv", stocks_db_df)
    ndx_data.set_comparison_group(symbols)
    date2 = ndx_data.get_last_day()

    ndxgroups_df, ndxsingle_df, ndxperfomrance_df = ndx_data.set_compare_dates(
        start_date, date2, symbols_single
    )
    ndxgroups_df.loc[ndxgroups_df["Group"] == "MANTA", "Group"] = group_name

    db.close()

    return ndxgroups_df, ndxsingle_df, ndxperfomrance_df


def get_symbols():
    db = Db()
    data_db = db.get_unique_values("Symbol")

    db.close()
    symbols = [symbol[0] for symbol in data_db]

    return symbols
