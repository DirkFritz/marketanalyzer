from dash import dcc, html
import dash_bootstrap_components as dbc
from datetime import datetime
import plotly.express as px
from components.symboltable import generate_data_dable, generateSymbolComponent
from db.dbqueries import get_idx_data, get_stock_data
import pandas as pd
from components.heatmap import generateHeatmap
from components.helper import get_index_symbols, map_symbol_asset_name
from dash.dash_table import FormatTemplate
from io import StringIO


def generate_update_groups():
    return (
        dbc.Row(
            [
                dbc.Col(generateSymbolComponent("")),
                dbc.Col(
                    generateSymbolComponent("-single"),
                ),
            ]
        ),
    )


def generateIndexGraph(
    start_date,
    end_date,
    market_cap_active,
    index_ndx100_active,
    symbols,
    symbols_single,
    data_stored,
    tabs_store,
):
    end_date = datetime.strptime(end_date + " 16:00:00", "%Y-%m-%d %H:%M:%S")
    start_date = datetime.strptime(start_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")

    idx_symbols = get_index_symbols(index_ndx100_active)

    symbols = [symbol for symbol in symbols if symbol in idx_symbols]

    ndxgroups_df = None
    ndxperfomrance_df = None
    stocks = None

    if (
        data_stored["Dates"][0] == str(start_date.date())
        and data_stored["Dates"][1] == str(end_date.date())
        and data_stored["Index"] == index_ndx100_active
    ):
        print("Saved Data")
        ndxgroups_df = pd.read_csv(StringIO(data_stored["Idx Groups"]))
        ndxperfomrance_df = pd.read_csv(StringIO(data_stored["Idx Performance"]))
        stocks = pd.read_csv(StringIO(data_stored["Stocks"]))
        ndxgroups_df["DateTime"] = pd.to_datetime(ndxgroups_df["DateTime"]).dt.date
        if stocks.empty == False:
            stocks["DateTime"] = pd.to_datetime(stocks["DateTime"]).dt.date
    else:
        ndxgroups_df, ndxperfomrance_df = get_idx_data(
            start_date.date(), end_date.date(), symbols, idx_symbols
        )

        stockgroups, stocks, draw_downs = get_stock_data(
            start_date.date(), end_date.date(), symbols_single
        )
        data_stored["Dates"] = [start_date.date(), end_date.date()]
        data_stored["Index"] = index_ndx100_active
        data_stored["Idx Groups"] = ndxgroups_df.to_csv()
        data_stored["Idx Performance"] = ndxperfomrance_df.to_csv()
        data_stored["Stocks"] = stocks.to_csv()

    selection_df = ndxgroups_df[
        (ndxgroups_df["DateTime"] >= start_date.date())
        & (ndxgroups_df["DateTime"] <= end_date.date())
    ]
    if stocks.empty == False:
        selection_single_df = stocks[
            (stocks["DateTime"] >= start_date.date())
            & (stocks["DateTime"] <= end_date.date())
        ][["Symbol", "DateTime", "Percent", "Market Cap"]]
        selection_single_df.rename(columns={"Symbol": "Group"}, inplace=True)

        selection_single_df["Average Percent"] = selection_single_df["Percent"]

        selection_df = pd.concat([selection_df, selection_single_df])

    fig_heat = generateHeatmap(ndxperfomrance_df)

    fig_line = None
    fig_bar = None

    selection_all = selection_df[selection_df["Group"] == "ALL"]

    selection_all = selection_all[
        selection_all["DateTime"] > selection_all["DateTime"].min()
    ]

    fig_line_winners_period = px.line(
        selection_all,
        x="DateTime",
        y="Winner Period",
        labels={"DateTime": "Zeit", "Winner Period": "Gewinner/Verlierer Prozent"},
        height=250,
    )

    fig_line_winners_period.update_layout(plot_bgcolor="RGB(255,255,255)")

    if market_cap_active:
        fig_line = px.line(
            selection_df,
            x="DateTime",
            y="Percent",
            color="Group",
            labels={"DateTime": "Zeit", "Percent": "Prozent"},
        )
        fig_line.update_layout(plot_bgcolor="RGB(255,255,255)")
        fig_bar = px.bar(
            ndxperfomrance_df,
            x="Symbol",
            y="Market Cap Change",
            labels={"Market Cap Change": "Marktkapitalisierung in USD"},
        )
        fig_bar.update(layout_showlegend=False)

        fig_bar.update_layout(plot_bgcolor="RGB(255,255,255)")

    else:
        fig_line = px.line(
            selection_df,
            x="DateTime",
            y="Average Percent",
            color="Group",
            labels={"DateTime": "Zeit", "Average Percent": "Prozent"},
        )
        fig_bar = px.bar(
            ndxperfomrance_df,
            x="Symbol",
            y="Percent",
            labels={"Percent": "Prozent"},
        )
        fig_bar.update(layout_showlegend=False)
        fig_line.update_layout(plot_bgcolor="RGB(255,255,255)")
        fig_bar.update_layout(plot_bgcolor="RGB(255,255,255)")
        fig_heat.update_layout(plot_bgcolor="RGB(255,255,255)")

    stocks_performance_df = ndxperfomrance_df[
        ["Symbol", "Open", "High", "Low", "Close", "Percent", "Volume"]
    ]

    stocks_performance_df["Percent"] = pd.to_numeric(stocks_performance_df["Percent"])
    stocks_performance_df["Percent"] = stocks_performance_df["Percent"].round(2) / 100

    stocks_performance_df = stocks_performance_df.rename(
        columns={"Percent": "Performance"}
    )

    stocks_performance_df = map_symbol_asset_name(stocks_performance_df)

    money = FormatTemplate.money(2)
    percentage = FormatTemplate.percentage(2)

    columns = [
        {"name": "Symbol", "id": "Symbol"},
        {"name": "Asset", "id": "Asset"},
        {"name": "Close", "id": "Close", "type": "numeric", "format": money},
        {
            "name": "Performance",
            "id": "Performance",
            "type": "numeric",
            "format": percentage,
        },
        {"name": "GICS Sektor", "id": "Sector"},
    ]

    return (
        dbc.Tabs(
            id="indexchart-tabs",
            active_tab=tabs_store["ActiveTab"],
            children=[
                dbc.Tab(
                    [
                        dcc.Graph(figure=fig_line),
                        dcc.Graph(figure=fig_line_winners_period),
                    ],
                    tab_id="Zeit",
                    label="Zeit",
                ),
                dbc.Tab(
                    [
                        dbc.Row(dcc.Graph(figure=fig_bar)),
                        dbc.Row(generate_data_dable(stocks_performance_df, columns)),
                    ],
                    tab_id="Absolut",
                    label="Absolut",
                ),
                dbc.Tab(
                    [
                        dbc.Row(dcc.Graph(figure=fig_heat)),
                        dbc.Row(generate_data_dable(stocks_performance_df, columns)),
                    ],
                    tab_id="Heat",
                    label="Heatmap",
                ),
            ],
        ),
        data_stored,
    )
