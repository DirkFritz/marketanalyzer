import pandas as pd


from db.db import Db
from db.helper import companies_data, historic_stock_data_date, companies_data
from analyzer.index import NdxData
from analyzer.stock import Stock


def getNdxData(start_date, end_date, symbols, ndx100_symbols):
    db = Db()

    stocks_db_df = historic_stock_data_date(db, start_date, ndx100_symbols)
    companies = companies_data(db)

    group_name = ""
    for symbol in symbols:
        group_name = group_name + symbol[0]

    ndx_data = NdxData(stocks_db_df, companies, ndx100_symbols)
    ndx_data.set_comparison_group(symbols)
    if end_date > ndx_data.get_last_day():
        end_date = ndx_data.get_last_day()

    ndxgroups_df, ndxperfomrance_df = ndx_data.set_compare_dates(start_date, end_date)
    ndxgroups_df.loc[ndxgroups_df["Group"] == "MANTA", "Group"] = group_name

    db.close()

    return ndxgroups_df, ndxperfomrance_df


def get_stock_data(start_date, end_date, symbols_single):
    db = Db()

    stocks_db_df = historic_stock_data_date(db, start_date, symbols_single)
    companies = companies_data(db)

    db.close()

    group_name = ""
    for symbol in symbols_single:
        group_name = group_name + symbol[0]

    stock_analyzer = Stock(stocks_db_df, companies, symbols_single)

    if stocks_db_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    if end_date > stock_analyzer.get_last_day():
        end_date = stock_analyzer.get_last_day()

    ndxgroups_df, ndxsingle_df = stock_analyzer.set_compare_dates(
        start_date, end_date, symbols_single
    )

    return ndxgroups_df, ndxsingle_df


def get_symbols():
    db = Db()
    data_db = db.get_unique_values("Symbol", "historic")

    db.close()
    symbols = [symbol[0] for symbol in data_db]

    return symbols
