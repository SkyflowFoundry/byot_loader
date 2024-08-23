import requests
import json
from datetime import datetime
from generateSchema import get_skyflow_params  # type:ignore

def createVault(vault_schema, directory, bearer_token):
    account_id, vault_url, WorkspaceID, Vault_Name, Vault_Table_Name, Management_URL, user_id, Records_Batch_Size = get_skyflow_params(directory, bearer_token)
    # use date/time for unique naming....
    today = datetime.today()
    vault_create_URL = Management_URL+'/v1/vaults'


    # the headers
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'content-type': 'application/json',
        'X-SKYFLOW-ACCOUNT-ID': account_id
    }
    #print(headers)

    # POST request --> create the vault.....
    print(f"Creating Skyflow vault...\n")
    response = requests.post(vault_create_URL, headers=headers, data=json.dumps(vault_schema))

    # Check the response
    if response.status_code == 200:
        tokenized_data = response.json()
        vault_id = tokenized_data["ID"]    #grab the vault_id
        print(f"Skyflow Vault Created: {vault_id}\n"+ vault_id)
        #print(json.dumps(tokenized_data, indent=2))     #debug
        input(f"\nPaused.... Press any key to continue...")    
        return response.status_code, vault_id
    else:
        print(f"Vault Creation Error: {response.status_code} - {response.text}")
        return response.status_code