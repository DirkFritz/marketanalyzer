import pandas as pd
import datetime
from analyzer.asset import Asset


pd.options.mode.chained_assignment = None  # default='warn'


class NdxData(Asset):
    def __init__(self, stocks_db_df, companies, symbols_stocks):
        super().__init__(stocks_db_df, companies, symbols_stocks)

    def get_last_day(self):
        return self.stocks_prices_df["DateTime"].max()

    def set_comparison_group(self, ticker_symbols=[]):

        self.ticker_symbols = ticker_symbols
        self.stocks = self.companies.loc[
            self.companies["Symbol"].isin(self.stocks_symbols)
        ]

        self.stocks_faang = self.stocks.loc[self.stocks["Symbol"].isin(ticker_symbols)]
        self.stocks_no_faang = self.stocks.loc[
            ~self.stocks["Symbol"].isin(ticker_symbols)
        ]

        self.stocks_no_faang_tech = self.stocks_no_faang.loc[
            self.stocks_no_faang["Sector"] == "Technology"
        ]
        self.stocks_no_faang_no_tech = self.stocks_no_faang.loc[
            self.stocks_no_faang["Sector"] != "Technology"
        ]

    def set_compare_dates(self, compare_date1, compare_date2):
        print(compare_date1)
        i = 0
        while i < 5:
            if self.stocks_prices_df["DateTime"].isin([compare_date1]).any() == False:
                compare_date1 = compare_date1 + datetime.timedelta(days=1)
            else:
                break
            i = i + 1
        i = 0
        while i < 5:
            if self.stocks_prices_df["DateTime"].isin([compare_date2]).any() == False:
                compare_date2 = compare_date2 + datetime.timedelta(days=1)
            else:
                break
            i = i + 1

        if len(self.ticker_symbols):
            self.create_market_cap_period(
                "MANTA", self.ticker_symbols, compare_date1, compare_date2
            )
        self.create_market_cap_period(
            "TECH",
            self.stocks_no_faang_tech["Symbol"].tolist(),
            compare_date1,
            compare_date2,
        )
        self.create_market_cap_period(
            "OTHERS",
            self.stocks_no_faang_no_tech["Symbol"].tolist(),
            compare_date1,
            compare_date2,
        )
        self.create_market_cap_period(
            "ALL",
            self.stocks["Symbol"].tolist(),
            compare_date1,
            compare_date2,
        )
        self.market_cap_period_df.loc[
            self.market_cap_period_df["Symbol"].isin(["GOOG", "GOOGL"]), ["Market Cap"]
        ] *= 0.5

        perfomrance_single_start = self.market_cap_period_df.loc[
            (
                self.market_cap_period_df["Symbol"].isin(self.stocks_symbols)
                & self.market_cap_period_df["Group"].isin(["ALL"])
                & self.market_cap_period_df["DateTime"].isin([compare_date1])
            ),
            :,
        ]

        perfomrance_single = self.market_cap_period_df.loc[
            (
                self.market_cap_period_df["Symbol"].isin(self.stocks_symbols)
                & self.market_cap_period_df["Group"].isin(["ALL"])
                & self.market_cap_period_df["DateTime"].isin([compare_date2])
            ),
            :,
        ]
        perfomrance_single_clean = perfomrance_single[
            perfomrance_single["Symbol"].isin(
                perfomrance_single_start["Symbol"].to_list()
            )
        ]

        perfomrance_single_clean.reset_index(drop=True, inplace=True)
        perfomrance_single_start.reset_index(drop=True, inplace=True)

        perfomrance_single_clean.loc[:, "Market Cap Change"] = 0
        perfomrance_single_clean.loc[:, "Market Cap Change"] = (
            perfomrance_single_clean["Market Cap"]
            - perfomrance_single_start["Market Cap"]
        )

        self.market_cap_start_all = self.market_cap_period_df[
            (
                self.market_cap_period_df["Symbol"].isin(self.stocks_symbols)
                & self.market_cap_period_df["Group"].isin(["ALL"])
                & self.market_cap_period_df["DateTime"].isin([compare_date1])
            )
        ]["Market Cap"].sum()

        self.market_cap_period_df.reset_index(drop=True, inplace=True)
        self.create_market_cap_period_groups("ALL")
        if len(self.ticker_symbols):
            self.create_market_cap_period_groups("MANTA")
        self.create_market_cap_period_groups("TECH")
        self.create_market_cap_period_groups("OTHERS")

        return (
            self.market_cap_period_groups,
            perfomrance_single_clean,
        )
