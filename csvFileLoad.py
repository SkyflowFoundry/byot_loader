import pandas as pd  # type: ignore
from getFile import getFile  # type: ignore
from get_bearer_token import getSignedJWT_fromfile, getBearerToken  # type: ignore
from generateSchema import build_vault_schema # type:ignore
from create_skyflow_vault import createVault # type:ignore
from createServiceAccount import generateSA  # type: ignore
from tableLoadData import batchLoad  # type: ignore

def csvFileProcessor():
    fullFile, directory = getFile('CSV')
    df = pd.read_csv(fullFile)   # Read the CSV data from the selected file
    print(f"CSV file: \n {fullFile} successfully uploaded")
    first_row = df.head(1)  # Get only the first data row - for type detect

    if len(first_row) >0:
            return first_row, df

def main():
    print(f"CSV Loader for Skyflow now running...\n")
    header_row, full_file  = csvFileProcessor()   # Get csv file headers and rows

    credsFile, directory = getFile('Skyflow Credentials')
    #Sign claims object, create private key
    signedJWT, creds, sa1_id = getSignedJWT_fromfile(credsFile)
    #print(signedJWT, creds)  #debug
    #Get bearer token
    bearerToken = getBearerToken(signedJWT, creds)
    #print(bearerToken)     #debug: bearerToken

    vaultSchema, AccountId = build_vault_schema(header_row, directory, bearerToken, sa1_id)
    print("Skyflow Vault Schema:  Generated")
    #print(json.dumps(vaultSchema, indent=2))    #debug: vault schema
    #create the skyflow vault
    status_code, vault_id = createVault(vaultSchema, directory, bearerToken)
    #create the Service Acount and get SA2 Jwt for the vault insert
    bearerTokenVault = generateSA(bearerToken, vault_id, AccountId)
    
    #Check the response - if success - load to vault
    if status_code == 200:
        print("Loading records into Skyflow Vault")
        loadSuccess = batchLoad(directory, full_file, bearerTokenVault, vault_id)
        if loadSuccess:
             print('SUCCESS: Run complete: All records successfully loaded to Skyflow')
        else:
             print('WARNING: Partial load (some errors) completed to Skyflow')
    else:
        print(f"Failed to load CSV records. Status code: {status_code}")

if __name__ == "__main__":
    main()
