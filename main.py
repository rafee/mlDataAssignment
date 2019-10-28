from concurrent import futures
from google.protobuf import struct_pb2
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
        return workloadQuery_pb2.ResponseForData(rfwId=2019)
    #     with status.context(context):
    #         response = workloadQuery_pb2.ResponseForData()
    #         return response
    # dataset_id = 'lake'
    # table_id = 'dvd_testing'
    # sql = """
    #     SELECT * FROM `assignemnt1-cloud-deployment.{dataset}.{table}` LIMIT 10 OFFSET 40
    #     """.format(dataset=dataset_id, table=table_id)
    # query_job = bigquery_client.query(sql)



def serve(port,shutdown_grace_duration):
    # try:
    #     # Set a timeout because queries could take longer than one minute.
    #     results = query_job.result(timeout=30)
    # except futures.TimeoutError:
    #     return flask.render_template("timeout.html", job_id=query_job.job_id)

    # return flask.render_template("query_result.html", results=results)

    # Previous code
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
    # print(f'server running on port {p}.')
    # server.wait_for_termination()


# serve()


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
