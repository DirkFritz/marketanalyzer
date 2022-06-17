from dash import (
    dcc,
    html,
)
from db.dbqueries import get_stock_data, date_picker_dates
from components.datepicker import generateDatePicker

import pandas as pd
import layouts.bestperfomer.callbacks
import dash_bootstrap_components as dbc
from components.symboltable import generateSymbolComponent
from components.indecreaseinput import generate_in_decrease_input


best_perfomrer = [
    html.Div(generateDatePicker(*date_picker_dates(), 30)),
    html.P(),
    dbc.Row(
        [
            dbc.Col(
                children=[
                    dbc.Label(
                        "Aktien/Aktiengruppen wählen",
                    ),
                    generateSymbolComponent(
                        "-bestperformer", ["NDX", "SPX"], ["NDX", "SPX"]
                    ),
                ],
            ),
            dbc.Col(
                [
                    dbc.Row(
                        id="best-performer-parameter",
                        children=[
                            dbc.Label(
                                "Merkmale", html_for="best-performer-features-switch"
                            ),
                            dbc.Checklist(
                                options=[
                                    {"label": "Performance", "value": 1},
                                    {"label": "Draw Down", "value": 2},
                                ],
                                value=[1, 2],
                                id="best-performer-features-switch",
                                inline=True,
                                switch=True,
                            ),
                        ],
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Gruppenanzahl"),
                            generate_in_decrease_input("-bestperformer"),
                        ]
                    ),
                ],
            ),
        ]
    ),
    dcc.Store(
        id="best-performer-dates",
        data={
            "start_date": "",
            "end_date": "",
        },
    ),
    dcc.Store(
        id="best-performer-features",
        data={
            "performance": True,
            "draw_down": True,
        },
    ),
    dcc.Store(
        id="best-performer-group-count",
        data={
            "group_count": 5,
        },
    ),
    html.P(),
    dbc.Spinner(
        html.Div(id="text-output"),
        color="primary",
        spinner_class_name="mb-auto",
    ),
    dcc.Store(
        id="symbol-group-value-bestperformer",
        data={"Symbol": []},
    ),
]
