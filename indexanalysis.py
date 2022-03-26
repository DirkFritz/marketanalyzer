from dash import (
    dcc,
    html,
    Input,
    Output,
    callback,
    callback_context,
    State,
)
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
import plotly.express as px
from dbqueries import getNdxData, get_symbols
from db import Db
import pandas as pd
import math


def generateDatePicker():
    db = Db()
    [min, max] = db.get_min_max_historic("date")
    print(min, max)
    db.close = ()
    start_date = datetime.today() - timedelta(days=30)
    return dcc.DatePickerRange(
        id="my-date-picker-range",
        min_date_allowed=min,
        max_date_allowed=max,
        start_date=start_date.date(),
        initial_visible_month=max,
        end_date=max,
    )


def generateGroupTable(data={}):

    df = pd.DataFrame(data)

    table = dbc.Table.from_dataframe(
        df,
        striped=True,
        bordered=True,
        hover=True,
        style={"width": "95%"},
    )
    return table


def generateGroupInput(comp_name=""):

    input = html.Div(
        [
            dbc.InputGroup(
                [
                    dcc.Dropdown(
                        id="symbol-group-input" + comp_name,
                        options=get_symbols(),
                        placeholder="Symbol...",
                        style={"width": "200px", "marginRight": "5px"},
                    ),
                    dbc.Button(
                        "Hinzufügen",
                        id="symbol-group-add" + comp_name,
                        color="primary",
                        className="me-1",
                    ),
                    dbc.Button(
                        "Update",
                        id="symbol-group-udpate" + comp_name,
                        color="primary",
                        className="me-1",
                    ),
                    dbc.Button(
                        "Löschen",
                        id="symbol-group-delete" + comp_name,
                        color="danger",
                        className="me-1",
                    ),
                ],
                style={"width": "100%"},
            ),
        ],
        className="col-xs-4",
    )

    return input


@callback(
    Output("symbol-group-container", "children"),
    Output("symbol-group-value", "data"),
    Output("symbol-group-input", "value"),
    Output("symbol-group-udpate", "disabled"),
    Input("symbol-group-add", "n_clicks"),
    Input("symbol-group-delete", "n_clicks"),
    State("symbol-group-input", "value"),
    State("symbol-group-value", "data"),
)
def update_group_table(add, delete, symbol, data):
    # print(add, delete, symbol, data)
    disable_update = False
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "symbol-group-add" in changed_id:
        if data is not None:
            if not symbol in data["Symbol"] and symbol is not None and not symbol == "":
                data["Symbol"].append(symbol)
    elif "symbol-group-delete" in changed_id:
        data = {"Symbol": []}
        # disable_update = True

    return generateGroupTable(data), data, "", disable_update


@callback(
    Output("symbol-group-container-single", "children"),
    Output("symbol-group-value-single", "data"),
    Output("symbol-group-input-single", "value"),
    Output("symbol-group-udpate-single", "disabled"),
    Input("symbol-group-add-single", "n_clicks"),
    Input("symbol-group-delete-single", "n_clicks"),
    State("symbol-group-input-single", "value"),
    State("symbol-group-value-single", "data"),
)
def update_single_table(add, delete, symbol, data):
    # print(add, delete, symbol, data)
    disable_update = False
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "symbol-group-add-single" in changed_id:
        if data is not None:
            if not symbol in data["Symbol"] and symbol is not None:
                data["Symbol"].append(symbol)
    elif "symbol-group-delete-single" in changed_id:
        data = {"Symbol": []}
        # disable_update = True

    return generateGroupTable(data), data, "", disable_update


index_analysis = [
    dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                [
                    dbc.DropdownMenuItem(
                        "Nasdasq100",
                        id="index_ndx100",
                        active=True,
                    ),
                ],
                label="Nasdasq100",
                id="index_analysis",
                color="primary",
                style={"marginRight": "10px"},
                in_navbar=True,
                disabled=True,
            ),
            dbc.DropdownMenu(
                [
                    dbc.DropdownMenuItem(
                        "Performance nach Marktkapitalisierung",
                        id="index_perfromance_market_cap",
                        active=True,
                    ),
                    dbc.DropdownMenuItem(
                        "Performance Gleichgewichtung",
                        id="index_perfromance_equal",
                    ),
                ],
                label="Datenauswertung",
                id="data_analysis",
                color="primary",
                in_navbar=True,
            ),
        ],
        # brand=" ",
        # brand_style={"text-align": "left"},
        color="light",
        # dark=True,
        # links_left=True,
    ),
    html.Div(generateDatePicker()),
    html.Div(dbc.Tabs(id="markectcap_percent", active_tab="Zeit")),
    dbc.Col(
        [
            generateGroupInput(),
            html.Div(generateGroupTable(), id="symbol-group-container"),
        ]
    ),
    dbc.Col(
        [
            generateGroupInput("-single"),
            html.Div(
                generateGroupTable({"Symbol": []}),
                id="symbol-group-container-single",
            ),
        ]
    ),
    dcc.Store(
        id="symbol-group-value",
        data={
            "Symbol": ["AAPL", "GOOG", "GOOGL", "MSFT", "NVDA", "TSLA"],
        },
    ),
    dcc.Store(
        id="symbol-group-value-single",
        data={
            "Symbol": [],
        },
    ),
]


@callback(
    Output("data_analysis", "label"),
    Output("index_perfromance_market_cap", "active"),
    Output("index_perfromance_equal", "active"),
    [
        Input("index_perfromance_market_cap", "n_clicks"),
        Input("index_perfromance_equal", "n_clicks"),
    ],
)
def set_index_analysis(n1, n2):

    id_lookup = {
        "index_perfromance_market_cap": "Performance nach Marktkapitalisierung",
        "index_perfromance_equal": "Performance Gleichgewichtung",
    }

    active_lookup = {
        "index_perfromance_market_cap": False,
        "index_perfromance_equal": False,
    }
    ctx = callback_context
    if (n1 is None and n2 is None) or not ctx.triggered:
        return (
            id_lookup["index_perfromance_market_cap"],
            True,
            False,
        )

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    active_lookup[button_id] = True
    return (
        id_lookup[button_id],
        active_lookup["index_perfromance_market_cap"],
        active_lookup["index_perfromance_equal"],
    )


def generateHeatmap(stocks_single_df):

    numShares = len(stocks_single_df["Percent"])

    heatmap_size = int(math.sqrt(numShares))
    i = 0
    performance_heatmap = []
    labels_heatmap = []

    if numShares > 100:
        stocks_single_df = stocks_single_df[stocks_single_df["Symbol"] != "GOOGL"]

    performance_stocks = stocks_single_df["Percent"]
    labels_stocks = stocks_single_df["Symbol"]

    i = 0
    for i in range(heatmap_size):
        j = 0
        row = []
        labels_row = []
        for j in range(heatmap_size):
            performance = performance_stocks.values[i * heatmap_size + j]
            performance_str = f"{performance:.2f}"

            row.append(performance)
            labels_row.append(
                labels_stocks.values[i * heatmap_size + j] + " " + performance_str
            )

        performance_heatmap.append(row)
        labels_heatmap.append(labels_row)

    return performance_heatmap, labels_heatmap


def generateIndexGraph(
    start_date, end_date, market_cap_active, symbols, symbols_single
):
    end_date = datetime.strptime(end_date + " 16:00:00", "%Y-%m-%d %H:%M:%S")
    start_date = datetime.strptime(start_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    ndxgroups_df, ndxsingle_df, ndxperfomrance_df = getNdxData(
        start_date.date(), symbols, symbols_single
    )

    selection_df = ndxgroups_df[
        (ndxgroups_df["DateTime"] >= start_date.date())
        & (ndxgroups_df["DateTime"] <= end_date.date())
    ]
    selection_single_df = ndxsingle_df[
        (ndxsingle_df["DateTime"] >= start_date.date())
        & (ndxsingle_df["DateTime"] <= end_date.date())
    ][["Symbol", "DateTime", "Percent", "Market Cap"]]

    selection_single_df["Average Percent"] = selection_single_df["Percent"]

    selection_single_df.rename(columns={"Symbol": "Group"}, inplace=True)

    selection_df = pd.concat([selection_df, selection_single_df])

    performance_heatmap, labels_heatmap = generateHeatmap(ndxperfomrance_df)

    fig_line = None
    fig_bar = None
    fig_heat = None

    if market_cap_active:
        fig_line = px.line(
            selection_df,
            x="DateTime",
            y="Percent",
            color="Group",
            labels={"DateTime": "Zeit", "Percent": "Prozent"},
        )
        fig_bar = px.bar(
            ndxperfomrance_df,
            x="Symbol",
            y="Market Cap Change",
            labels={"Market Cap Change": "Marktkapitalisierung in USD"},
        )
        fig_bar.update(layout_showlegend=False)

        fig_heat = px.imshow(
            performance_heatmap,
            color_continuous_scale=[(0, "red"), (0.5, "#474747"), (1, "#00FF00")],
            aspect="auto",
            zmin=-20,
            zmax=20,
        )
        fig_heat.update_traces(
            text=labels_heatmap, texttemplate="%{text}", hovertemplate=None
        )

        fig_line.update_layout(plot_bgcolor="RGB(255,255,255)")
        fig_bar.update_layout(plot_bgcolor="RGB(255,255,255)")
        fig_heat.update_layout(plot_bgcolor="RGB(255,255,255)")

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
            # color="Symbol",
            labels={"Percent": "Prozent"},
        )
        fig_bar.update(layout_showlegend=False)
        fig_heat = px.imshow(
            performance_heatmap,
            color_continuous_scale=[(0, "red"), (0.5, "#474747"), (1, "#00FF00")],
            aspect="auto",
            zmin=-20,
            zmax=20,
        )
        fig_heat.update_traces(
            text=labels_heatmap, texttemplate="%{text}", hovertemplate=None
        )
        fig_line.update_layout(plot_bgcolor="RGB(255,255,255)")
        fig_bar.update_layout(plot_bgcolor="RGB(255,255,255)")
        fig_heat.update_layout(plot_bgcolor="RGB(255,255,255)")

    return [
        dbc.Tab(dcc.Graph(figure=fig_line), tab_id="Zeit", label="Zeit"),
        dbc.Tab(dcc.Graph(figure=fig_bar), tab_id="Absolut", label="Absolut"),
        dbc.Tab(dcc.Graph(figure=fig_heat), tab_id="Heat", label="Heatmap"),
    ]


@callback(
    Output("markectcap_percent", "children"),
    Input("my-date-picker-range", "start_date"),
    Input("my-date-picker-range", "end_date"),
    Input("index_perfromance_market_cap", "active"),
    State("symbol-group-value", "data"),
    State("symbol-group-value-single", "data"),
)
def update_ndx_market_cap(
    start_date,
    end_date,
    market_cap_active,
    data,
    data_single,
):
    try:

        graph = generateIndexGraph(
            start_date,
            end_date,
            market_cap_active,
            data["Symbol"],
            data_single["Symbol"],
        )
    except Exception as e:
        print(e)
        return None

    return graph
