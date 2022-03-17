from google.cloud import storage
import dash
from dash import dcc
import layout


import dash_bootstrap_components as dbc

dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_app.title = "LT AI"
app = dash_app.server

db = Db()
[min, max] = db.get_min_max_historic("date")
print(min, max)


dash_app.layout = layout.main_layout


def main():
    dash_app.run_server(debug=False)


if __name__ == "__main__":
    main()
