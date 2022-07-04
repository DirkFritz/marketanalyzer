from lib2to3.pygram import Symbols
import pandas as pd
from db.helper import companies_data
from db.db import Db


def get_index_symbols(ndx):
    idx_symbols = None
    if ndx:
        idx_symbols = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")[3][
            "Ticker"
        ].to_list()
    else:
        idx_data = pd.read_html(
            "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        )[0]
        idx_data["Symbol"] = idx_data["Symbol"].str.replace(".", " ", regex=True)

        idx_symbols = idx_data["Symbol"].to_list()

    return idx_symbols


def map_symbol_asset_name(data):
    db = Db()
    companies = companies_data(db)

    data["Asset"] = ""
    data = data.sort_values(["Symbol"]).reset_index(drop=True)
    assets = companies[companies["Symbol"].isin(data["Symbol"])]
    assets = assets.sort_values(["Symbol"]).reset_index(drop=True)
    data["Asset"] = assets["Name"]
    data["Sector"] = assets["Sector"]
    data["Industry"] = assets["Industry"]

    data.loc[data["Sector"] == "", "Sector"] = "N/A"

    db.close()
    return data
