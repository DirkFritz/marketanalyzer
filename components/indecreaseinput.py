from dash import (
    dcc,
    html,
    callback_context,
)
import dash_bootstrap_components as dbc


def generate_in_decrease_input(comp_name):

    input = html.Div(
        [
            dbc.InputGroup(
                [
                    dbc.Button(
                        "-",
                        id="indecrease-group-minus" + comp_name,
                        color="primary",
                        className="me-1",
                    ),
                    dbc.Input(
                        id="indecrease-group-input" + comp_name,
                        placeholder="5",
                        type="numeric",
                        disabled=True,
                    ),
                    dbc.Button(
                        "+",
                        id="indecrease-group-plus" + comp_name,
                        color="primary",
                        className="me-1",
                    ),
                ],
                style={"width": "20%"},
            ),
        ],
        className="col-xs-4",
    )

    return input
