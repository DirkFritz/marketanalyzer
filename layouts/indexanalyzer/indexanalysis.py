from dash import (
    dcc,
    html,

)
import dash_bootstrap_components as dbc
from db.db import Db

from components.symboltable import generateSymbolComponent
from components.datepicker import generateDatePicker
import layouts.indexanalyzer.callbacks


def date_picker_dates():
    db = Db()
    [min, max] = db.get_min_max("historic", "date")
    db.close()

    return min, max


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
    html.P(
        dbc.Spinner(
            html.Div(dbc.Tabs(id="markectcap_percent", active_tab="Zeit")),
            color="primary",
        )
    ),
    dbc.Col(generateSymbolComponent("")),
    dbc.Col(
        generateSymbolComponent("-single"),
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
