from dash import (
    dcc,
)
import dash_bootstrap_components as dbc
from datetime import datetime
import plotly.express as px
from dbqueries import getNdxData, get_stock_data
import pandas as pd
from components.heatmap import generateHeatmap


def generateIndexGraph(
    start_date,
    end_date,
    market_cap_active,
    index_ndx100_active,
    symbols,
    symbols_single,
):
    end_date = datetime.strptime(end_date + " 16:00:00", "%Y-%m-%d %H:%M:%S")
    start_date = datetime.strptime(start_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")

    idx_symbols = None
    if index_ndx100_active:
        idx_symbols = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")[3][
            "Ticker"
        ].to_list()
    else:
        idx_data = pd.read_html(
            "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        )[0]
        idx_data["Symbol"] = idx_data["Symbol"].str.replace(".", " ", regex=True)

        idx_symbols = idx_data["Symbol"].to_list()

    symbols = [symbol for symbol in symbols if symbol in idx_symbols]

    ndxgroups_df, ndxperfomrance_df = getNdxData(
        start_date.date(), end_date.date(), symbols, idx_symbols
    )

    stockgroups, stocks = get_stock_data(
        start_date.date(), end_date.date(), symbols_single
    )

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

    return [
        dbc.Tab(dcc.Graph(figure=fig_line), tab_id="Zeit", label="Zeit"),
        dbc.Tab(dcc.Graph(figure=fig_bar), tab_id="Absolut", label="Absolut"),
        dbc.Tab(dcc.Graph(figure=fig_heat), tab_id="Heat", label="Heatmap"),
    ]
