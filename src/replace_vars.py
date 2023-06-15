import argparse
import json
import os


def parse_args():
    parser = argparse.ArgumentParser(description="Upload graphql datamodels to CDF")
    parser.add_argument(
        "--file", required=True,
        type=str)
    parser.add_argument(
        "--space", required=True,
        type=str)
    parser.add_argument(
        "--version", required=True,
        type=str)
    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.file, 'r') as file :
        filedata = file.read()


    
    newdata = filedata.replace('$SPACE', args.space)
    newdata = newdata.replace('$VERSION', args.version)

    if filedata != newdata:
        print(f"Updated {args.file} with version: {args.version} and space {args.space}")
        with open(args.file, 'w') as file:
            file.write(newdata)
    else:
        print("No space or version variables in data model")


if __name__ == "__main__":
    main()
