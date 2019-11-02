import time

import grpc
import workloadQuery_pb2
import workloadQuery_pb2_grpc

server_ip='dataset.mohammadrafee.com:80'
# server_ip='35.202.153.101:80'

channel = grpc.insecure_channel(server_ip)
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
