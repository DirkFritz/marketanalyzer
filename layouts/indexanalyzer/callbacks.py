from dash import (
    Input,
    Output,
    callback,
    callback_context,
    State,
)

from components.symboltable import update_table
from components.indexcharts import generateIndexGraph


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
    Output("index_analysis", "label"),
    Output("index_ndx100", "active"),
    Output("index_spx", "active"),
    [
        Input("index_ndx100", "n_clicks"),
        Input("index_spx", "n_clicks"),
    ],
)
def set_index(n1, n2):

    id_lookup = {
        "index_ndx100": "Nasdaq100",
        "index_spx": "S&P500",
    }

    active_lookup = {
        "index_ndx100": False,
        "index_spx": False,
    }
    ctx = callback_context
    if (n1 is None and n2 is None) or not ctx.triggered:
        return (
            id_lookup["index_ndx100"],
            True,
            False,
        )

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    active_lookup[button_id] = True
    return (
        id_lookup[button_id],
        active_lookup["index_ndx100"],
        active_lookup["index_spx"],
    )


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
    return update_table("symbol-group-add", "symbol-group-delete", symbol, data)


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
    return update_table(
        "symbol-group-add-single", "symbol-group-delete-single", symbol, data
    )


@callback(
    Output("markectcap_percent", "children"),
    Input("my-date-picker-range", "start_date"),
    Input("my-date-picker-range", "end_date"),
    Input("index_perfromance_market_cap", "active"),
    Input("index_ndx100", "active"),
    Input("symbol-group-udpate-single", "n_clicks"),
    Input("symbol-group-udpate", "n_clicks"),
    State("symbol-group-value", "data"),
    State("symbol-group-value-single", "data"),
)
def update_ndx_market_cap(
    start_date,
    end_date,
    market_cap_active,
    index_ndx100_active,
    update_group,
    update_single,
    data,
    data_single,
):
    try:

        graph = generateIndexGraph(
            start_date,
            end_date,
            market_cap_active,
            index_ndx100_active,
            data["Symbol"],
            data_single["Symbol"],
        )
    except Exception as e:
        print(e)
        return None

    return graph
