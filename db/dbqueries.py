import pandas as pd


from db.db import Db
from db.helper import companies_data, historic_stock_data_date, companies_data
from analyzer.index import Index
from analyzer.stock import Stock


def get_idx_data(start_date, end_date, symbols, ndx100_symbols):
    db = Db()

    stocks_db_df = historic_stock_data_date(db, start_date, ndx100_symbols)
    db.close()

    db = Db()

    companies = companies_data(db)

    db.close()

    group_name = ""
    for symbol in symbols:
        group_name = group_name + symbol[0]

    print("Start Performance Stock Calculation ")
    ndx_data = Index(stocks_db_df, companies, ndx100_symbols)
    ndx_data.set_comparison_group(symbols)
    if end_date > ndx_data.get_last_day():
        end_date = ndx_data.get_last_day()

    print("Start Performance Index Calculation ")
    ndxgroups_df, ndxperfomrance_df = ndx_data.set_compare_dates(start_date, end_date)
    ndxgroups_df.loc[ndxgroups_df["Group"] == "MANTA", "Group"] = group_name

    print(ndxgroups_df)

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
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    if end_date > stock_analyzer.get_last_day():
        end_date = stock_analyzer.get_last_day()

    stock_groups, stock_single = stock_analyzer.set_compare_dates(
        start_date, end_date, symbols_single
    )
    draw_downs = stock_analyzer.get_max_draw_down(start_date, end_date, symbols_single)

    return stock_groups, stock_single, draw_downs


def get_symbols(allowed_symbols=[], custom_symbols=[]):
    db = Db()
    data_db = db.get_unique_values("Symbol", "historic")

    db.close()
    symbols = [
        symbol[0]
        for symbol in data_db
        if allowed_symbols == [] or symbol in allowed_symbols
    ]
    symbols = symbols + custom_symbols

    return symbols


def date_picker_dates():
    db = Db()
    [min, max] = db.get_min_max("historic", "date")
    db.close()

    return min, max
