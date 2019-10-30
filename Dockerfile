FROM gcr.io/google_appengine/python
 
WORKDIR /datasetquery
 
ADD *.py /datasetquery/
ADD *.proto /datasetquery/
RUN pip install grpcio grpcio-tools google-cloud-bigquery
RUN python -m grpc_tools.protoc \
	workloadQuery.proto \
	-I. --python_out=. --grpc_python_out=.

EXPOSE 8000
 
ENTRYPOINT ["python", "/datasetquery/workloadQueryServer.py"]

