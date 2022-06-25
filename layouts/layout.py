import layouts.indexanalyzer.indexanalysis as indexanalysis
import layouts.bestperfomer.bestperformer as bestperformer
import dash_bootstrap_components as dbc
from dash import dcc, callback, Input, Output, html
from components.symboltable import generateSymbolComponent


index_analysis_layout = dbc.Row([indexanalysis.index_analysis])

best_performer_layout = dbc.Row(bestperformer.best_perfomrer)


main_layout = html.Div(
    [
        # represents the browser address bar and doesn't render anything
        dcc.Location(id="url", refresh=False),
        # content will be rendered in this element
        # html.Div(id="page-content"),
        dbc.Row(id="page-content"),
    ]
)


@callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
)
def display_page(pathname):
    print(pathname)
    if pathname == "/indexanalysis":
        return indexanalysis.index_analysis
    return best_performer_layout
