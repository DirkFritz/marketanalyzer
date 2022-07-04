import math
import plotly.express as px


def generateHeatmap(stocks_single_df):

    numShares = len(stocks_single_df["Percent"])

    heatmap_size = int(math.sqrt(numShares))
    i = 0
    performance_heatmap = []
    labels_heatmap = []

    if numShares > 100:
        stocks_single_df = stocks_single_df[stocks_single_df["Symbol"] != "GOOGL"]

    performance_stocks = stocks_single_df["Percent"]
    labels_stocks = stocks_single_df["Symbol"]
    heatmap_size = max(heatmap_size, 10)
    i = 0
    for i in range(heatmap_size):
        j = 0
        row = []
        labels_row = []
        for j in range(heatmap_size):
            index = i * heatmap_size + j
            if index < len(performance_stocks.values):
                performance = performance_stocks.values[index]
                performance_str = f"{performance:.2f}"

                row.append(performance)
                labels_row.append(labels_stocks.values[index] + " " + performance_str)
            else:
                row.append(0)
                labels_row.append("-")

        performance_heatmap.append(row)
        labels_heatmap.append(labels_row)

    fig_heat = px.imshow(
        performance_heatmap,
        color_continuous_scale=[(0, "red"), (0.5, "#474747"), (1, "#00FF00")],
        aspect="auto",
        zmin=-20,
        zmax=20,
    )
    fig_heat.update_traces(
        text=labels_heatmap, texttemplate="%{text}", hovertemplate=None
    )
    fig_heat.update_layout(plot_bgcolor="RGB(255,255,255)")

    return fig_heat
