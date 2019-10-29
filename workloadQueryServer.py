from concurrent import futures
# from google.protobuf import struct_pb2
import argparse
import time

import grpc
import workloadQuery_pb2
import workloadQuery_pb2_grpc
import status

from google.cloud import bigquery

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
bigquery_client = bigquery.Client()


class WorkloadQueryMockServer(workloadQuery_pb2_grpc.WorkloadQueryServicer):
    def GetSamples(self, request, context):
        response = workloadQuery_pb2.ResponseForData()
        response.rfwId = request.rfwId

        project_id = 'assignemnt1-cloud-deployment'
        dataset_id = 'lake'
        table_id = request.benchmarkType.source.lower()+'_'+request.benchmarkType.type
        sql = """
        SELECT {metric} FROM `{project}.{dataset}.{table}` 
        LIMIT {endpoint} OFFSET {startpoint}
        """.format(metric=request.workloadMetric, project=project_id,
                   dataset=dataset_id, table=table_id, startpoint=request.batchUnit *
                   (request.batchId-1), endpoint=request.batchUnit*request.batchSize)
        # print(sql)
        query_job = bigquery_client.query(sql)
        try:
            # Set a timeout because queries could take longer than one minute.
            results = query_job.result(timeout=30)
        except futures.TimeoutError:
            return workloadQuery_pb2.ResponseForData(rfwId=2021)
        for result in results:
            getattr(response,"samples").append(result[0])
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
