FROM gcr.io/google_appengine/python
 
WORKDIR /datasetquery
 
ADD *.py /datasetquery/
ADD *.proto /datasetquery/
# ADD Assignemnt1-Cloud-Deployment-8838ebbde098.json $HOME
# RUN export GOOGLE_APPLICATION_CREDENTIALS="$HOME/Assignemnt1-Cloud-Deployment-8838ebbde098.json"
RUN pip install grpcio grpcio-tools google-cloud-bigquery
RUN python -m grpc_tools.protoc \
	workloadQuery.proto \
	-I. --python_out=. --grpc_python_out=.

EXPOSE 8000
 
ENTRYPOINT ["python", "/datasetquery/Server.py"]