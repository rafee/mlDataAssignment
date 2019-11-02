VENV="grpc-python"
workon $VENV

python -m grpc_tools.protoc \
    --include_imports \
    --include_source_info \
    --proto_path=. \
    --descriptor_set_out=api_descriptor.pb \
    --python_out=. \
    --grpc_python_out=. \
    workloadQuery.proto

gcloud endpoints services deploy api_descriptor.pb api_config.yaml

docker build -t grpc-workload-server .