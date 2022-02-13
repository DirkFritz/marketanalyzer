from flask import Flask, render_template, url_for, request, redirect
from google.cloud import storage
import pandas as pd

from ndxdata import NdxData
from datetime import datetime

app = Flask(__name__)

ndx_data = None


def update():
    ndx_data = NdxData(
        "gs://lt-capital.de/nasdaq_screener.csv", "gs://lt-capital.de/ndxdata.csv"
    )
    # ndx_data = NdxData("gs://lt-capital.de/nasdaq_screener.csv", "ndxdata.csv")
    ndx_data.set_comparison_group(["AAPL", "GOOG", "GOOGL", "MSFT", "NVDA", "TSLA"])

    return ndx_data


@app.route("/", methods=["GET"])
def index():

    plot = None

    ndx_data = update()
    if ndx_data != None:

        date1 = datetime.strptime("2021/11/15 15:30:00", "%Y/%m/%d %H:%M:%S")
        date2 = datetime.strptime("2022/02/11 15:30:00", "%Y/%m/%d %H:%M:%S")
        ndx_data.set_compare_dates(date1, date2)
        plot = ndx_data.save_plot()

    return render_template("index.html", contents=plot)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
