from dash import html
import indexanalysis

main_layout = html.Div(
    children=[
        html.H4(children="Nasdaq Relative Rendite"),
        html.Div(
            children=[
                "Zeitraum auswählen",
            ]
        ),
        indexanalysis.index_analysis,
        html.A(
            "Datenschutzerklärung", href="https://lt-capital.de/datenschutzerklaerung/"
        ),
        html.Br(),
        html.A("Impressum", href="https://lt-capital.de/impressum/"),
        html.Br(),
        html.A("LT Capital", href="https://lt-capital.de/"),
    ]
)
