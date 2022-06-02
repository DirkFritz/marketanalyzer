import dash
import layouts.layout as layout


import dash_bootstrap_components as dbc


dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_app.title = "LT AI"
dash_app.config.suppress_callback_exceptions = True

dash_app.validation_layout = layout.index_analysis_layout
dash_app.layout = layout.main_layout

app = dash_app.server


def main():

    dash_app.run_server(debug=True)


if __name__ == "__main__":
    main()
