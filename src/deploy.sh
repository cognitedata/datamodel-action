#!/bin/bash

cdf signin $INPUT_PROJECT --client-id=$INPUT_CLIENTID --client-secret=$INPUT_CLIENTSECRET --cluster=$INPUT_CLUSTER --tenant=$INPUT_TENANTID
python src/replace_vars.py --file=$INPUT_MODELFILE --space=$INPUT_SPACE --version=$INPUT_VERSION

datamodels=$(cdf data-models list | awk 'NR>2 {print $4$6}')
datamodels_list=()

while IFS= read -r datamodel; do
    datamodel=$(echo "$datamodel" | awk '{$1=$1};1')  # Remove leading/trailing whitespaces
    datamodel=${datamodel// /}  # Eliminate all whitespaces
    if [[ -n "$datamodel" ]]; then
    datamodels_list+=("$datamodel")  # Append datamodel to the list
    fi
done <<< "$datamodels"
echo "All data models in datamodels list:"

found=false
for item in "${datamodels_list[@]}"; do
    echo "datamodel=$item"
    if [[ $item == ${{ inputs.modelName }}${{ inputs.space }} ]]; then
    echo "checking if item in model name"
    found=true
    break
    fi
done

echo "::set-output name=found::$found"
if $found; then
    echo "Model name $INPUT_MODELNAME exists in datamodels"
else
    echo "Model name $INPUT_MODELNAME does not exist in datamodels, create and publish"
    if cdf data-models create "$INPUT_MODELNAME" --external-id=$INPUT_MODELNAME --space=$INPUT_SPACE --verbose --interactive=false; then
        echo "Data model created successfully."
    else
        echo "Error occurred while creating the data model. Skipping."
    fi
fi

cdf data-models publish --external-id=$INPUT_MODELNAME --file=$INPUT_MODELFILE --space=$INPUT_SPACE --version=$INPUT_VERSION --verbose --interactive=false

