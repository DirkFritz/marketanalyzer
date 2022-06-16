from faulthandler import disable
from dash import html, Input, Output, callback, callback_context, State, html
import datetime
from db.dbqueries import get_stock_data
import pandas as pd
from algos.bestperformer import BestPerformer
import numpy as np
import dash_bootstrap_components as dbc
from components.symboltable import generateSymbolComponent, update_table


def generate_performer_group(performer, group_count):

    tabs = []
    for i in range(group_count):
        performer_group = performer[performer["Labels"] == i][
            ["Symbol", "Performance", "Draw Down"]
        ]

        performer_group = performer_group.reset_index(drop=True)
        performer_group = performer_group.set_index("Symbol")

        tab_content = dbc.Card(
            dbc.CardBody(
                [
                    dbc.Table.from_dataframe(
                        performer_group,
                        striped=True,
                        bordered=True,
                        hover=True,
                        index=True,
                    )
                ]
            ),
            className="mt-3",
        )
        tabs.append(dbc.Tab(tab_content, label="Gruppe " + str(i + 1)))

    return dbc.Tabs(tabs)


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
                performance = stock[stock["DateTime"] == end_date]["Percent"].values[0]
            if features["draw_down"]:
                draw_down = stocks_draw_down[symbol]
            best_perfomrer_data_set.append([symbol, performance, draw_down])

    return pd.DataFrame(
        best_perfomrer_data_set, columns=["Symbol", "Performance", "Draw Down"]
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
    symbols = list(set(symbols))

    print(symbols_all)
    stock_groups, stocks_performance, stocks_draw_down = get_stock_data(
        start_date,
        end_date,
        symbols_all,
    )

    best_perfomrer_data_set = generate_dataset(
        stocks_performance, stocks_draw_down, symbols_all, end_date, features
    )
    best_performer = BestPerformer()
    performer = best_performer.find_perfomrer(best_perfomrer_data_set, group_count)

    performer_overview = []
    for i in range(group_count):
        print("Gruppe ", i)
        performance_max = performer[performer["Labels"] == i]["Performance"].max()
        draw_down_min = performer[performer["Labels"] == i]["Draw Down"].min()
        performance_mean = performer[performer["Labels"] == i]["Performance"].mean()
        draw_down_mean = performer[performer["Labels"] == i]["Draw Down"].mean()

        performer_overview.append(
            [
                i + 1,
                performance_max,
                draw_down_min,
                round(performance_mean, 2),
                round(draw_down_mean, 2),
            ]
        )

    performer_overview = pd.DataFrame(
        performer_overview,
        columns=[
            "Gruppe",
            "Maximale Performance",
            "Minimaler Draw Down",
            "Durchschnitt Performance",
            "Durchschnitt Draw Down",
        ],
    )
    performer_overview = performer_overview.set_index("Gruppe")
    return [
        dbc.Table.from_dataframe(
            performer_overview,
            striped=True,
            bordered=True,
            hover=True,
            index=True,
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
        print(minus, plus, group_count, input)
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
        print(features_selection)

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
    print("Update", symbols)

    return determ_best_perfomer(dates, features, group_count, symbols)
