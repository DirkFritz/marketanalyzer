from dash import dcc, html, Input, Output, callback, callback_context
import dash_bootstrap_components as dbc
from datetime import datetime
import plotly.express as px
from dbqueries import getNdxData

index_analysis = [
    dcc.DatePickerRange(
        id="my-date-picker-range",
        min_date_allowed=min,
        max_date_allowed=max,
        start_date="2022-01-03",
        initial_visible_month=max,
        end_date=max,
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
    ),
    html.Div(id="markectcap_percent"),
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


@callback(
    Output("markectcap_percent", "children"),
    Input("my-date-picker-range", "start_date"),
    Input("my-date-picker-range", "end_date"),
    Input("index_perfromance_market_cap", "active"),
    Input("index_perfromance_equal", "active"),
)
def update_ndx_market_cap(start_date, end_date, market_cap_active, equal_active):
    end_date = datetime.strptime(end_date + " 16:00:00", "%Y-%m-%d %H:%M:%S")
    start_date = datetime.strptime(start_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    ndxgroups_df = getNdxData(start_date.date())

    selection_df = ndxgroups_df[
        (ndxgroups_df["DateTime"] >= start_date.date())
        & (ndxgroups_df["DateTime"] <= end_date.date())
    ]
    fig = None
    if market_cap_active:
        fig = px.line(
            selection_df,
            x="DateTime",
            y="Percent",
            color="Group",
            labels={"DateTime": "Zeit", "Percent": "Prozent"},
            title="Prozentualer Verlauf Marktkapitalisierung",
        )
        fig.update_layout(plot_bgcolor="RGB(210,210,210)")
    else:
        fig = px.line(
            selection_df,
            x="DateTime",
            y="Average Percent",
            color="Group",
            labels={"DateTime": "Zeit", "Average Percent": "Prozent"},
            title="Prozentualer Verlauf gleich gewichtet",
        )
        fig.update_layout(plot_bgcolor="RGB(210,210,210)")
    return dcc.Graph(figure=fig)
