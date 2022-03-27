import dash
import layout

import dash_bootstrap_components as dbc

dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_app.title = "LT AI"
app = dash_app.server


dash_app.layout = layout.main_layout


def main():
    dash_app.run_server(debug=True)


if __name__ == "__main__":
    main()
