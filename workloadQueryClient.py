import time
import argparse

import grpc
import workloadQuery_pb2
import workloadQuery_pb2_grpc

import requests
from tabulate import tabulate

_GRPC_ENDPOINT = 'grpc.dataset.mohammadrafee.com:80'
_HTTP_ENDPOINT = 'http://rest.dataset.mohammadrafee.com/v1/mldata'

def generateId():
    return 0

def textRequest(rfwid, args):
    r = requests.get(_HTTP_ENDPOINT, params=args, headers={'rfwid':str(rfwid)})
    if r.status_code == 200:
        return r.json()
    else:
        print('An error has occurred during GET request')
        exit()

def binaryRequest(rfwid, args):
    channel = grpc.insecure_channel(_GRPC_ENDPOINT)
    client = workloadQuery_pb2_grpc.WorkloadQueryStub(channel)

    bt = workloadQuery_pb2.RequestForWorkload.BenchmarkType(source=args['source'], type=args['type'])
    rfw = workloadQuery_pb2.RequestForWorkload(rfwId=rfwid, benchmarkType=bt, workloadMetric=args['workloadMetric'], batchUnit=args['batchUnit'], batchId=args['batchId'], batchSize=args['batchSize'])

    r = client.GetSamples(rfw)
    return {'lastbatchId': r.lastBatchId, 'rfwid': r.rfwId, 'samples': r.samples}



parser = argparse.ArgumentParser(description='Retrieve workload data for machine learning purposes.')
parser.add_argument('source', metavar='<benchmark>', type=str, help='The benchmark from which the data is sourced.')
parser.add_argument('type', metavar='<set>', type=str, help='The set (train/test) from which the data is sourced.')
parser.add_argument('workloadMetric', metavar='<metric>', type=str, help='The metric ("cpu", "networkIn", "networkOut", "memory", "finalTarget") to retrieve for each sample.')
parser.add_argument('--binary', '-b', action='store_true', help='Use binary (de)serialization instead of text (de)serialization.')
parser.add_argument('--batch-unit', '-u', metavar='<unit>', dest='batchUnit', type=int, default=32, help='The number of samples included in each batch.')
parser.add_argument('--batch-id', '-i', metavar='<id>', dest='batchId', type=int, default=1, help='The index of the first batch to retrieve.')
parser.add_argument('--batch-size', '-s', metavar='<size>', dest='batchSize', type=int, default=1, help='The number of batches to retrieve.')

args = vars(parser.parse_args())
print(args)

rfwId = generateId()

binary = args['binary']
del args['binary']

if binary:
    result = binaryRequest(rfwId, args)
else:
    result = textRequest(rfwId, args)

table = tabulate(map(lambda s: [s], result['samples']), showindex=True, headers=['Sample', f"Value({args['workloadMetric']})"])

print(f'Client rfw id: {result["rfwid"]}')
print(f'Last batch id is {result["lastbatchId"]}')
print(table)

exit()