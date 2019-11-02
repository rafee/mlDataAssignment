import time
import argparse

import grpc
import workloadQuery_pb2
import workloadQuery_pb2_grpc

import requests
from tabulate import tabulate

_SERVER_ADDR = ''
_HTTP_ENDPOINT = 'http://mlquery.mohammadrafee.com/v1/'

def generateId():
    return 0

def textRequest(args):
    params =  f"sources/{args['benchmark']}/types/{args['set']}/metrics/{args['metric']}/batch_units/{args['batch_unit']}/batch_id/{args['batch_id']}/batch_size/{args['batch_size']}"
    url = _HTTP_ENDPOINT + params
    print('getting from ' + url)
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        print('An error has occurred during GET request')
        exit()

def binaryRequest(args):
    channel = grpc.insecure_channel(_SERVER_ADDR)
    client = workloadQuery_pb2_grpc.WorkloadQueryStub(channel)

    request = workloadQuery_pb2.RequestForWorkload()
    testResponse = client.GetSamples(request)
    return {}



parser = argparse.ArgumentParser(description='Retrieve workload data for machine learning purposes.')
parser.add_argument('benchmark', metavar='benchmark', type=str, help='The benchmark from which the data is sourced.')
parser.add_argument('set', metavar='set', type=str, help='The set (train/test) from which the data is sourced.')
parser.add_argument('metric', metavar='metric', type=str, help='The metric ("cpu", "networkIn", "networkOut", "memory", "finalTarget") to retrieve for each sample.')
parser.add_argument('--binary', '-b', action='store_true', help='Use binary (de)serialization instead of text (de)serialization.')
parser.add_argument('--batch-unit', '-u', metavar='unit', type=int, default=32, help='The number of samples included in each batch.')
parser.add_argument('--batch-id', '-i', metavar='id', type=int, default=0, help='The index of the first batch to retrieve.')
parser.add_argument('--batch-size', '-s', metavar='size', type=int, default=1, help='The number of batches to retrieve.')

args = vars(parser.parse_args())
print(args)
#example

rfwId = generateId()

if args['binary']:
    result = binaryRequest(args)
else:
    result = textRequest(args)

batches =
table = tabulate(map(lambda s: [s], result['samples']), showindex=True, headers=['Sample', f"Value({args['metric']})"])

print(f'Client rfw id: {result["rfwid"]}')
print(f'Last batch id is {result["lastbatchId"]}')
print(table)

exit()