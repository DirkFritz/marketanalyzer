from faulthandler import disable
from dash import html, Input, Output, callback, callback_context, State, html, dcc
import datetime
from db.dbqueries import get_stock_data
import pandas as pd
from algos.bestperformer import BestPerformer
import numpy as np
import dash_bootstrap_components as dbc
from components.symboltable import generate_data_dable, update_table
import plotly.express as px
from dash.dash_table import FormatTemplate
from components.helper import map_symbol_asset_name


def generate_performer_group(performer, group_count):

    tabs = []
    percentage = FormatTemplate.percentage(2)

    performer = map_symbol_asset_name(performer)

    columns = [
        {"name": "Symbol", "id": "Symbol"},
        {"name": "Asset", "id": "Asset"},
        {
            "name": "Performance",
            "id": "Performance",
            "type": "numeric",
            "format": percentage,
        },
        {
            "name": "Draw-Down",
            "id": "Draw-Down",
            "type": "numeric",
            "format": percentage,
        },
        {"name": "GICS Sektor", "id": "Sector"},
    ]

    for i in range(group_count):
        performer_group = performer[performer["Labels"] == i][
            ["Symbol", "Asset", "Performance", "Draw-Down", "Sector"]
        ]
        performer_group_sector_count = (
            performer_group["Sector"].value_counts().reset_index()
        )
        fig_pie = px.pie(performer_group_sector_count, values="Sector", names="index")

        tab_content = dbc.Card(
            dbc.CardBody(
                dbc.Row(
                    [
                        dbc.Col(generate_data_dable(performer_group, columns), width=7),
                        dbc.Col(dcc.Graph(figure=fig_pie), width=5),
                    ]
                )
            ),
            className="mt-3",
        )
        tabs.append(
            dbc.Tab(
                tab_content, label="Gruppe " + str(i + 1), tab_id="Gruppe " + str(i + 1)
            )
        )

    return dbc.Tabs(tabs, active_tab="Gruppe 1")


def generate_dataset(stocks_performance, stocks_draw_down, symbols, end_date, features):
    if end_date > stocks_performance["DateTime"].max():
        end_date = stocks_performance["DateTime"].max()

    best_perfomrer_data_set = []
    for symbol in symbols:
        stock = stocks_performance[stocks_performance["Symbol"] == symbol]
        if not stock.empty:
            draw_down = 0.0
            performance = 0.0

            if features["performance"]:
                # print([stock["DateTime"] == end_date], end_date)
                performance = stock[stock["DateTime"] == end_date]["Percent"].values[0]
            if features["draw_down"]:
                draw_down = stocks_draw_down[symbol]
            best_perfomrer_data_set.append([symbol, performance, draw_down])

    return pd.DataFrame(
        best_perfomrer_data_set, columns=["Symbol", "Performance", "Draw-Down"]
    )


def determ_best_perfomer(dates, features, group_count, symbols):

    start_date = dates["start_date"]
    end_date = dates["end_date"]
    group_count = group_count["group_count"]

    if start_date == "":
        end_date = (datetime.datetime.today() - datetime.timedelta(days=1)).date()
        start_date = end_date - datetime.timedelta(days=30)
    else:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    if symbols["Symbol"] == []:
        return html.Div()

    symbols_all = []
    if "NDX" in symbols["Symbol"]:
        symbols_all = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")[3][
            "Ticker"
        ].to_list()
    if "SPX" in symbols["Symbol"]:
        idx_data = pd.read_html(
            "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        )[0]
        idx_data["Symbol"] = idx_data["Symbol"].str.replace(".", " ", regex=True)
        symbols_all = symbols_all + idx_data["Symbol"].to_list()
    symbols_all = list(set(symbols_all))

    stock_groups, stocks_performance, stocks_draw_down = get_stock_data(
        start_date,
        end_date,
        symbols_all,
    )

    best_perfomrer_data_set = generate_dataset(
        stocks_performance, stocks_draw_down, symbols_all, end_date, features
    )
    # print(best_perfomrer_data_set)
    best_performer = BestPerformer()
    performer = best_performer.find_perfomrer(best_perfomrer_data_set, group_count)

    performer_overview = []
    for i in range(group_count):
        performance_mean = (
            performer[performer["Labels"] == i]["Performance"].mean() / 100
        )
        draw_down_mean = performer[performer["Labels"] == i]["Draw-Down"].mean() / 100
        size_group = performer[performer["Labels"] == i]["Draw-Down"].shape[0]

        performer_overview.append(
            [i + 1, round(performance_mean, 2), round(draw_down_mean, 2), size_group]
        )

    performer_overview = pd.DataFrame(
        performer_overview,
        columns=[
            "Group",
            "Performance",
            "Draw-Down",
            "Size",
        ],
    )
    performer["Performance"] = performer["Performance"] / 100
    performer["Draw-Down"] = performer["Draw-Down"] / 100

    performer_overview_chart = pd.melt(
        performer_overview[["Group", "Performance", "Draw-Down"]],
        id_vars=["Group"],
        var_name="feature",
        value_name="value",
    )

    performer_overview_chart["value"] = performer_overview_chart["value"] * 100

    fig_bar = px.bar(
        performer_overview_chart,
        x="Group",
        y="value",
        color="feature",
        barmode="group",
        labels={"Group": "Gruppe", "value": "Prozent", "feature": "Merkmal"},
    )
    fig_bar.update_layout(plot_bgcolor="RGB(255,255,255)")

    percentage = FormatTemplate.percentage(2)

    columns = [
        {
            "name": "Gruppe",
            "id": "Group",
            "type": "numeric",
        },
        {
            "name": "Gruppengröße",
            "id": "Size",
            "type": "numeric",
        },
        {
            "name": "Performance",
            "id": "Performance",
            "type": "numeric",
            "format": percentage,
        },
        {
            "name": "Draw-Down",
            "id": "Draw-Down",
            "type": "numeric",
            "format": percentage,
        },
    ]

    return [
        dbc.Row(
            [
                dbc.Col(
                    generate_data_dable(
                        performer_overview,
                        columns,
                    )
                ),
                dbc.Col(dcc.Graph(figure=fig_bar)),
            ]
        ),
        generate_performer_group(performer, group_count),
    ]


@callback(
    Output("best-performer-dates", "data"),
    Input("my-date-picker-range", "start_date"),
    Input("my-date-picker-range", "end_date"),
    State("best-performer-dates", "data"),
)
def update_best_performer_dates(start_date, end_date, data):
    try:
        data["start_date"] = start_date
        data["end_date"] = end_date
    except Exception as e:
        print(e)
        return None

    return data


@callback(
    Output("indecrease-group-input-bestperformer", "value"),
    Output("best-performer-group-count", "data"),
    Input("indecrease-group-minus-bestperformer", "n_clicks"),
    Input("indecrease-group-plus-bestperformer", "n_clicks"),
    State("best-performer-group-count", "data"),
)
def update_group_count(minus, plus, group_count):
    try:
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]
        if "indecrease-group-minus-bestperformer" in changed_id:
            if group_count["group_count"] > 0:
                group_count["group_count"] = group_count["group_count"] - 1
        if "indecrease-group-plus-bestperformer" in changed_id:
            group_count["group_count"] = group_count["group_count"] + 1

    except Exception as e:
        print(e)

    return group_count["group_count"], group_count


@callback(
    Output("best-performer-features", "data"),
    Output("symbol-group-udpate-bestperformer", "disabled"),
    Input("best-performer-features-switch", "value"),
    State("best-performer-features", "data"),
)
def update_feature_selection(features_selection, data):
    try:

        update_disabled = False
        if 1 in features_selection:
            data["performance"] = True
        else:
            data["performance"] = False
        if 2 in features_selection:
            data["draw_down"] = True
        else:
            data["draw_down"] = False
        if features_selection == []:
            update_disabled = True

    except Exception as e:
        print(e)
        return None

    return data, update_disabled


@callback(
    Output("symbol-group-container-bestperformer", "children"),
    Output("symbol-group-value-bestperformer", "data"),
    Output("symbol-group-input-bestperformer", "value"),
    Input("symbol-group-add-bestperformer", "n_clicks"),
    Input("symbol-group-delete-bestperformer", "n_clicks"),
    State("symbol-group-input-bestperformer", "value"),
    State("symbol-group-value-bestperformer", "data"),
)
def update_symbol_table(add, delete, symbol, data):

    data_table, data, input_value, update_disable = update_table(
        "symbol-group-add-bestperformer",
        "symbol-group-delete-bestperformer",
        symbol,
        data,
    )
    return data_table, data, input_value


@callback(
    Output("text-output", "children"),
    Input("symbol-group-udpate-bestperformer", "n_clicks"),
    State("best-performer-dates", "data"),
    State("best-performer-features", "data"),
    State("best-performer-group-count", "data"),
    State("symbol-group-value-bestperformer", "data"),
)
def update_single_table(update, dates, features, group_count, symbols):

    return determ_best_perfomer(dates, features, group_count, symbols)
