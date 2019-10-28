import time

import grpc
import workloadQuery_pb2
import workloadQuery_pb2_grpc

channel = grpc.insecure_channel('localhost:8000')
client = workloadQuery_pb2_grpc.WorkloadQueryStub(channel)

request = workloadQuery_pb2.RequestForWorkload()
testResponse = client.GetSamples(request)
print(testResponse.rfwId)