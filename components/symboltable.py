from dash import dcc, html, callback_context, dash_table
import dash_bootstrap_components as dbc
from db.dbqueries import get_symbols
import pandas as pd


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


def generateDataTable(data={}):

    df = pd.DataFrame(data)

    table = dash_table.DataTable(
        df.to_dict("records"),
        [{"name": i, "id": i} for i in df.columns],
        style_cell={
            "textAlign": "left",
            "font-family": '"Helvetica Neue", Helvetica, Arial, sans-serif',
        },
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        page_current=0,
        page_size=10,
    )
    return table


def generateGroupInput(comp_name="", allowed_symbols=[], custom_symbols=[]):

    input = html.Div(
        [
            dbc.InputGroup(
                [
                    dcc.Dropdown(
                        id="symbol-group-input" + comp_name,
                        options=get_symbols(allowed_symbols, custom_symbols),
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


def update_table(add_id, delete_id, symbol, data):
    disable_update = False
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if add_id in changed_id:
        if data is not None:
            if not symbol in data["Symbol"] and symbol is not None and not symbol == "":
                data["Symbol"].append(symbol)
    elif delete_id in changed_id:
        data = {"Symbol": []}
        # disable_update = True

    return generateGroupTable(data), data, "", disable_update


def generateSymbolComponent(id="", allowed_symbols=[], custom_symbols=[]):
    return html.Div(
        children=[
            generateGroupInput(id, allowed_symbols, custom_symbols),
            html.Div(generateGroupTable(), id="symbol-group-container" + id),
        ]
    )
