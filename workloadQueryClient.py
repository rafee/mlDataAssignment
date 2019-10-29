import time

import grpc
import workloadQuery_pb2
import workloadQuery_pb2_grpc

channel = grpc.insecure_channel('localhost:8000')
client = workloadQuery_pb2_grpc.WorkloadQueryStub(channel)

request = workloadQuery_pb2.RequestForWorkload()
request.rfwId = 202020
request.benchmarkType.source = "DVD"
request.benchmarkType.type = "testing"
request.workloadMetric = "CPUUtilization_Average"
request.batchUnit = 5
request.batchId = 6
request.batchSize = 2
testResponse = client.GetSamples(request)
print(testResponse.rfwId)
