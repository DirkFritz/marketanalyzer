from flask import Flask, render_template, url_for, request, redirect
from google.cloud import storage

app = Flask(__name__)



@app.route('/', methods=['GET'])
def index():
   storage_client = storage.Client()
   bucket = storage_client.get_bucket('lt-capital.de')
   # Then do other things...
   blob = bucket.get_blob('testfile.txt')
   print(blob.download_as_bytes())
   
   return render_template('index.html', contents=blob.download_as_bytes())


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)