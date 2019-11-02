from concurrent import futures
import argparse
import time
import csv

import grpc
import workloadQuery_pb2
import workloadQuery_pb2_grpc

from google.cloud import storage

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def parse_method(BUCKET='assignment1-data', FILE='Input-Data/NDBench-testing.csv'):
    client = storage.Client()
    bucket = client.get_bucket(BUCKET)
    blob = bucket.get_blob(FILE)
    csv_data = blob.download_as_string()
    read_data = csv.reader(csv_data.decode("utf-8").splitlines())

    return list(read_data)

class WorkloadQueryMockServer(workloadQuery_pb2_grpc.WorkloadQueryServicer):
    def GetSamples(self, request, context):
        response = workloadQuery_pb2.ResponseForData()
        response.rfwId = request.rfwId
        benchmarkType_source = request.benchmarkType.source
        benchmarkType_type = request.benchmarkType.type
        workloadMetric = request.workloadMetric
        batchUnit = request.batchUnit
        batchId = request.batchId
        batchSize = request.batchSize

        bucket = 'assignment1-data'
        file = 'Input-Data/'+benchmarkType_source+'-'+benchmarkType_type+'.csv'
        loaded_data = parse_method(bucket, file)
        loaded_data = loaded_data[1:]
        
        starting_index = (batchId-1)*batchUnit
        finishing_index = (batchId+batchSize-1)*batchUnit
        lookup_dict = {'CPU': 0, 'NetworkIn': 1, 'NetworkOut': 2, 'Memory': 3}
        metricIndex = lookup_dict[workloadMetric]
        outputs = [data[metricIndex] for data in loaded_data]
        outputs = outputs[starting_index:finishing_index]
        getattr(response,"samples").append(outputs)
        return response


def serve(port, shutdown_grace_duration):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    workloadQuery_pb2_grpc.add_WorkloadQueryServicer_to_server(
        WorkloadQueryMockServer(), server)
    p = server.add_insecure_port('[::]:{}'.format(port))
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(shutdown_grace_duration)


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--port', type=int, default=8000, help='The port to listen on')
    parser.add_argument(
        '--shutdown_grace_duration', type=int, default=5,
        help='The shutdown grace duration, in seconds')

    args = parser.parse_args()

    serve(args.port, args.shutdown_grace_duration)