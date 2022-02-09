from flask import Flask, render_template, url_for, request, redirect
from google.cloud import storage
import pandas as pd

from ndxdata import NdxData

app = Flask(__name__)


@app.route('/update', methods=['GET'])
def update():
   storage_client = storage.Client()
   bucket = storage_client.get_bucket('lt-capital.de')
   # Then do other things...
   blob = bucket.get_blob('ndxdata.csv')
   blob.download_to_filename("ndxdata.csv")
   print("Update NDX Data")

   blob = bucket.get_blob('nasdaq_screener.csv')
   blob.download_to_filename("nasdaq_screener.csv")
   print("Update NDX Sceener Data")

   return "Update done"




@app.route('/', methods=['GET'])
def index():
   
   ndx_data = NdxData("nasdaq_screener.csv","ndxdata.csv")

   ndx_data.set_comparison_group(['AAPL','GOOG','GOOGL','MSFT','NVDA','TSLA'])
   ndx_data.set_compare_dates(20211115, 20220204)
   ndx_data.save_plot()
   
   return render_template('index.html', contents="Test")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)