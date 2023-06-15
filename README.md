# Deploy Cognite datamodel action
This action deploys a DataModel to Cognite

## Inputs
1. `modelName` - name of model
2. `space` - space 
3. `version` - version string to use

4. `project` 
5. `clientId`
6. `clientSecret`
7. `cluster`
8. `tenantId` - either use tenantId (with AAD) 
9. `tokenUrl` - for other idPs

If you have $VERSION or $SPACE in your graphql it will be replaced with supplied parameters before deploy.
