from flask import Flask, jsonify, request
import csv
from google.cloud import storage

app = Flask(__name__)


def parse_method(BUCKET='assignment1-data', FILE='Input-Data/NDBench-testing.csv'):
    client = storage.Client()
    bucket = client.get_bucket(BUCKET)
    blob = bucket.get_blob(FILE)
    csv_data = blob.download_as_string()
    read_data = csv.reader(csv_data.decode("utf-8").splitlines())

    return list(read_data)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/v1/mldata/', methods=["GET"])
def GetSamples():
    RFWID = request.headers.get('rfwid')
    benchmarkType_source = request.args['source']
    benchmarkType_type = request.args['type']
    workloadMetric = request.args['workloadMetric']
    batchUnit = request.args['batchUnit']
    batchId = request.args['batchId']
    batchSize = request.args['batchSize']
    bucket = 'assignment1-data'
    file = 'Input-Data/'+benchmarkType_source+'-'+benchmarkType_type+'.csv'
    loaded_data = parse_method(bucket, file)
    loaded_data = loaded_data[1:]  # Skipping first row
    batchId = int(batchId)
    batchUnit = int(batchUnit)
    batchSize = int(batchSize)
    starting_index = (batchId-1)*batchUnit
    finishing_index = (batchId+batchSize-1)*batchUnit
    lookup_dict = {'CPU': 0, 'NetworkIn': 1, 'NetworkOut': 2, 'Memory': 3}
    metricIndex = lookup_dict[workloadMetric]
    outputs = [data[metricIndex] for data in loaded_data]
    outputs = outputs[starting_index:finishing_index]
    return jsonify(rfwid=RFWID, lastbatchId=batchId+batchSize, samples=outputs)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
