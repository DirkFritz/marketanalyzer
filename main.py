from google.cloud import storage
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
from db import Db
from ndxdata import NdxData

import dash_bootstrap_components as dbc

dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_app.title = "LT AI"
app = dash_app.server

db = Db()
[min, max] = db.get_min_max_historic("date")
print(min, max)


def getNdxData(start_date):
    db = Db()
    data_db = db.select_historic_date(start_date)
    stocks_db_df = pd.DataFrame(
        columns=["Symbol", "DateTime", "Open", "Close", "High", "Low", "Volume"]
    )
    stocks_db_df = pd.concat(
        [
            stocks_db_df,
            pd.DataFrame(
                data_db,
                columns=[
                    "Symbol",
                    "DateTime",
                    "Open",
                    "Close",
                    "High",
                    "Low",
                    "Volume",
                ],
            ),
        ]
    )

    ndx_data = NdxData("gs://lt-capital.de/nasdaq_screener.csv", stocks_db_df)
    ndx_data.set_comparison_group(["AAPL", "GOOG", "GOOGL", "MSFT", "NVDA", "TSLA"])
    date2 = ndx_data.get_last_day()

    ndxgroups_df = ndx_data.set_compare_dates(start_date, date2)
    print(ndxgroups_df)

    db.close()

    return ndxgroups_df


@dash_app.callback(
    Output("markectcap_percent", "children"),
    Input("my-date-picker-range", "start_date"),
    Input("my-date-picker-range", "end_date"),
)
def update_ndx_market_cap(start_date, end_date):
    end_date = datetime.strptime(end_date + " 16:00:00", "%Y-%m-%d %H:%M:%S")
    start_date = datetime.strptime(start_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    ndxgroups_df = getNdxData(start_date.date())
    selection_df = ndxgroups_df[
        (ndxgroups_df["DateTime"] >= start_date.date())
        & (ndxgroups_df["DateTime"] <= end_date.date())
    ]

    fig = px.line(
        selection_df,
        x="DateTime",
        y="Percent",
        color="Group",
        labels={"DateTime": "Zeit", "Percent": "Prozent"},
        title="Prozentualer Verlauf Marktkapitalisierung",
    )
    fig.update_layout(plot_bgcolor="RGB(210,210,210)")

    fig2 = px.line(
        selection_df,
        x="DateTime",
        y="Average Percent",
        color="Group",
        labels={"DateTime": "Zeit", "Average Percent": "Prozent"},
        title="Prozentualer Verlauf gleich gewichtet",
    )
    fig2.update_layout(plot_bgcolor="RGB(210,210,210)")
    return dcc.Graph(figure=fig), dcc.Graph(figure=fig2)


dash_app.layout = html.Div(
    children=[
        html.H1(children="Nasdaq Relative Rendite"),
        html.Div(
            children=[
                "Zeitraum auswählen",
            ]
        ),
        html.Div(
            children=[
                dcc.DatePickerRange(
                    id="my-date-picker-range",
                    min_date_allowed=min,
                    max_date_allowed=max,
                    start_date=min,
                    initial_visible_month=max,
                    end_date=max,
                ),
                html.Div(id="markectcap_percent"),
            ]
        ),
        html.A(
            "Datenschutzerklärung", href="https://lt-capital.de/datenschutzerklaerung/"
        ),
        html.Br(),
        html.A("Impressum", href="https://lt-capital.de/impressum/"),
        html.Br(),
        html.A("LT Capital", href="https://lt-capital.de/"),
    ]
)


def main():
    dash_app.run_server(debug=False)


if __name__ == "__main__":
    main()
