import argparse
import os

from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from cognite.client.data_classes.data_modeling import SpaceApply
from cognite.client.data_classes.data_modeling import DataModelApply


def parse_args():
    parser = argparse.ArgumentParser(description="Upload graphql datamodels to CDF")
    parser.add_argument(
        "--file", required=False,
        default=os.environ.get("INPUT_MODELFILE", None),
        type=str)
    parser.add_argument(
        "--space", required=False,
        default=os.environ.get("INPUT_SPACE", None),
        type=str)
    parser.add_argument(
        "--model-name", required=False,
        default=os.environ.get("INPUT_MODELNAME", None),
        type=str)
    parser.add_argument(
        "--model-external-id", required=False,
        default=os.environ.get("INPUT_MODELEXTERNALID", None),
        type=str)
    parser.add_argument(
        "--model-description", required=False,
        default=os.environ.get("INPUT_MODELDESCRIPTION", None),
        type=str)
    parser.add_argument(
        "--version", required=False,
        default=os.environ.get("INPUT_VERSION", None),
        type=str)
    parser.add_argument(
        "--client-id", required=False,
        default=os.environ.get("INPUT_CLIENTID", None),
        type=str)
    parser.add_argument(
        "--client-secret", required=False,
        default=os.environ.get("INPUT_CLIENTSECRET", None),
        type=str)
    parser.add_argument(
        "--cluster", required=False,
        default=os.environ.get("INPUT_CLUSTER", None),
        type=str)
    parser.add_argument(
        "--project", required=False,
        default=os.environ.get("INPUT_PROJECT", None),
        type=str)
    parser.add_argument(
        "--tenant-id", required=False,
        default=os.environ.get("INPUT_TENANTID", None),
        type=str)
    parser.add_argument(
        "--token-url", required=False,
        default=os.environ.get("INPUT_TOKENURL", None),
        type=str)
    parser.add_argument(
        "--scopes", required=False,
        default=os.environ.get("INPUT_SCOPES", None),
        type=str)
    parser.add_argument(
        "--audience", required=False,
        default=os.environ.get("INPUT_AUDIENCE", None),
        type=str)

    return parser.parse_args()

def print_args(args):
    print(f"file: {args.file}")
    print(f"space: {args.space}")
    print(f"model_name: {args.model_name}")
    print(f"model_external_id: {args.model_external_id}")
    print(f"model_description: {args.model_description}")
    print(f"version: {args.version}")
    print(f"client_id: {args.client_id}")
    print(f"cluster: {args.cluster}")
    print(f"project: {args.project}")
    print(f"tenant_id: {args.tenant_id}")
    print(f"token_url: {args.token_url}")
    print(f"scopes: {args.scopes}")
    print(f"audience: {args.audience}")


def get_cognite_client(args):

    if args.tenant_id:
        token_url = f"https://login.microsoftonline.com/{args.tenant_id}/oauth2/v2.0/token"
    else:
        token_url = args.token_url

    scopes = args.scopes if args.scopes else f"https://{args.cluster}.cognitedata.com/.default"

    oauth_provider = OAuthClientCredentials(
        token_url=token_url,
        client_id=args.client_id,
        client_secret=args.client_secret,
        scopes=scopes.split(' '),
        #Any additional IDP-specific token args. e.g.
        audience=args.audience,
    )

    cnf = ClientConfig(
        client_name="datamodel-deploy",
        project=args.project,
        credentials=oauth_provider,
        base_url=f"https://{args.cluster}.cognitedata.com",
        debug=False
    )

    return CogniteClient(config=cnf)

def main():
    args = parse_args()
    print_args(args)
    client = get_cognite_client(args)

    with open(args.file, 'r') as file :
        filedata = file.read()

    external_id = args.model_external_id if args.model_external_id else args.model_name

    dml = filedata.replace('$SPACE', args.space)
    dml = dml.replace('$VERSION', args.version)

    if filedata != dml:
        print(f"Updated {args.file} with version: {args.version} and space {args.space}")
    else:
        print("No space or version variables in data model")

    space = client.data_modeling.spaces.retrieve(space=args.space)

    if not space:    
        print(f"Create space: {args.space}")
        client.data_modeling.spaces.apply([SpaceApply(space=space, description=space, name=space)])

    print(f"Update Data Model: {args.model_name} Version: {args.version}")
    data_model = [DataModelApply(
                        space=args.space,
                        external_id=external_id,
                        name=args.model_name,
                        version=args.version,
                        description=args.model_description)
                    ]
    print(data_model)
    client.data_modeling.data_models.apply(data_model)

if __name__ == "__main__":
    main()
