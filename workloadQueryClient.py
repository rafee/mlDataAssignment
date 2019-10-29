import time
import argparse

import grpc
import workloadQuery_pb2
import workloadQuery_pb2_grpc

_SERVER_ADDR = 'localhost:5051'

parser = argparse.ArgumentParser(description='Retrieve workload data for machine learning purposes.')
parser.add_argument('benchmark', metavar='benchmark', type=str, help='The benchmark from which the data is sourced.')
parser.add_argument('set', metavar='set', type=str, help='The set (train/test) from which the data is sourced.')
parser.add_argument('--binary', '-b', action='store_true', help='Use binary (de)serialization instead of text (de)serialization.')
parser.add_argument('--batch-unit', '-u', metavar='unit', type=int, nargs=1, default=32, help='The number of samples included in each batch.')
parser.add_argument('--batch-id', '-i', metavar='id', type=int, nargs=1, default=0, help='The index of the first batch to retrieve.')
parser.add_argument('--batch-size', '-s', metavar='size', type=int, nargs=1, default=1, help='The number of batches to retrieve.')
parser.add_argument('--metric', '-m', metavar='metric', type=str, nargs='+', default=["cpu", "networkIn", "networkOut", "memory", "finalTarget"], help='The metrics ("cpu", "networkIn", "networkOut", "memory", "finalTarget") to retrieve for each sample.')

args = vars(parser.parse_args())

rfwId = generateId()

if(args['binary']):
    result = textRequest(args)
else:
    result = binaryRequest(args)

print(f'Client rfw id: {result['rfwId']}')
print(f'Last batch id is {result['lastBatchId']}')
for index, batch in enumerate(result['samples']):
    print(f'Batch {args['batch_id'] + index}:', end='')
    for metric in args['metric']:
        print(f'\t{metric}')
    for sample in batch:
        print('\t\t')
        for metric in sample:
            print(f'\t{metric}')
exit()

def generateId():
    return 0

def textRequest(args):
    return {}

def binaryRequest(args):
    channel = grpc.insecure_channel(_SERVER_ADDR)
    client = workloadQuery_pb2_grpc.WorkloadQueryStub(channel)

    request = workloadQuery_pb2.RequestForWorkload()
    testResponse = client.GetSamples(request)
    return {}

