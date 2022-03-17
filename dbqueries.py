import pandas as pd


from db import Db
from ndxdata import NdxData


def getNdxData(start_date):
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

    ndx_data = NdxData("gs://lt-capital.de/nasdaq_screener.csv", stocks_db_df)
    ndx_data.set_comparison_group(["AAPL", "GOOG", "GOOGL", "MSFT", "NVDA", "TSLA"])
    date2 = ndx_data.get_last_day()

    ndxgroups_df = ndx_data.set_compare_dates(start_date, date2)
    print(ndxgroups_df)

    db.close()

    return ndxgroups_df
