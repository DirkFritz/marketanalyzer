from flask import Flask, render_template, url_for, request, redirect
from google.cloud import storage
import pandas as pd

import plotly
import plotly.express as px
import json

app = Flask(__name__)


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )


def get_plot(path):

    ndxgroups = pd.read_csv(path)

    fig1 = px.line(
        ndxgroups,
        x="DateTime",
        y="Percent",
        color="Group",
        labels={"DateTime": "Zeit", "Percent": "Prozent"},
    )
    fig1.update_layout(paper_bgcolor="#c5a089", plot_bgcolor="RGB(210,210,210)")

    fig2 = px.line(
        ndxgroups,
        x="DateTime",
        y="Average Percent",
        color="Group",
        labels={"DateTime": "Zeit", "Average Percent": "Prozent"},
    )
    fig2.update_layout(paper_bgcolor="#c5a089", plot_bgcolor="RGB(210,210,210)")

    return [
        json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder),
        json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder),
    ]


@app.route("/", methods=["GET"])
def index():

    plot = None

    plot = get_plot("gs://lt-capital.de/ndxgroups.csv")

    return render_template("index.html", contents=plot)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
