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
        default=os.environ.get("INPUT_MODELEXTERNALID", os.environ.get("INTPUT_MODELNAME", None)),
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

def get_cognite_client(args):

    if args.tenant_id:
        token_url = f"https://login.microsoftonline.com/{args.tenant_id}/oauth2/v2.0/token"
    else:
        token_url = args.token_url

    if args.scopes:
        scopes = args.scopes
    else:
        scopes = f"https://{args.cluster}.cognitedata.com/.default"

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
    client = get_cognite_client(args)

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
