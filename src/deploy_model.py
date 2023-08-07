import argparse
import os

from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from cognite.client.data_classes.data_modeling import SpaceApply
from cognite.client.data_classes.data_modeling import DataModelApply


def parse_args():
    parser = argparse.ArgumentParser(description="Upload graphql datamodels to CDF")
    parser.add_argument(
        "--file", required=True,
        default=os.get("INPUT_MODELFILE", None),
        type=str)
    parser.add_argument(
        "--space", required=True,
        default=os.get("INPUT_SPACE", None),
        type=str)
    parser.add_argument(
        "--model-name", reuired=True,
        default=os.get("INTPUT_MODELNAME", None)
        type=str)
    parser.add_argument(
        "--model-external-id", reuired=True,
        default=os.get("INPUT_MODEL_EXTERNAL_ID", os.get("INTPUT_MODELNAME", None))
        type=str)
    parser.add_argument(
        "--model-description", reuired=True,
        default=os.get("INPUT_MODEL_DESCRIPTION", None),
        type=str)
    parser.add_argument(
        "--version", required=True,
        default=os.get("INPUT_VERSION", None)
        type=str)

    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.file, 'r') as file :
        filedata = file.read()
    
    dml = filedata.replace('$SPACE', args.space)
    dml = dml.replace('$VERSION', args.version)

    if filedata != dml:
        print(f"Updated {args.file} with version: {args.version} and space {args.space}")
    else:
        print("No space or version variables in data model")

    print("Initialize CogniteClient")
    client = CogniteClient()

    space = client.data_modeling.spaces.retrieve(space=args.space)

    if not space:    
        print(f"Create space: {args.space}")
        client.data_modeling.spaces.apply([SpaceApply(space=space, description=space, name=space)])

    print(f"Update Data Model: {args.model_name} Version: {args.version}")
    data_model = [DataModelApply(
                        space=args.space,
                        external_id=args.model_external_id,
                        name=args.model_name,
                        version=args.version,
                        description=args.model_description)
                    ]
    client.data_modeling.data_models.apply(data_model)

if __name__ == "__main__":
    main()
