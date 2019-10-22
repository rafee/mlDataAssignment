from concurrent import futures

import grpc
import workloadQuery_pb2
import workloadQuery_pb2_grpc

class WorkloadQueryMockServer(workloadQuery_pb2_grpc.WorkloadQueryServicer):
    def GetSamples(self, request, context):
        return workloadQuery_pb2.ResponseForData(rfwId=2019)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    workloadQuery_pb2_grpc.add_WorkloadQueryServicer_to_server(WorkloadQueryMockServer(), server)
    p = server.add_insecure_port('[::]:5051')
    server.start()
    print(f'server running on port {p}.')
    server.wait_for_termination()

serve()