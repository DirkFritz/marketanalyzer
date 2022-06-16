import pandas as pd


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
