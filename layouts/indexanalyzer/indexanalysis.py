from dash import (
    dcc,
    html,
)
import dash_bootstrap_components as dbc
from db.dbqueries import date_picker_dates


from components.datepicker import generateDatePicker
import layouts.indexanalyzer.callbacks


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
                    dbc.DropdownMenuItem(
                        "S&P500",
                        id="index_spx",
                        active=False,
                    ),
                ],
                label="Nasdasq100",
                id="index_analysis",
                color="primary",
                style={"marginRight": "10px"},
                in_navbar=True,
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
    html.Div(generateDatePicker(*date_picker_dates(), 30)),
    html.P(),
    dbc.Spinner(
        html.Div(
            id="markectcap_percent",
        ),
        color="primary",
        spinner_class_name="mb-auto",
        delay_show=100,
    ),
    html.Div(
        id="indexchart-groups",
        children=[
            dbc.Row(id="symbol-group-udpate-single"),
            dbc.Row(id="symbol-group-udpate"),
        ],
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
