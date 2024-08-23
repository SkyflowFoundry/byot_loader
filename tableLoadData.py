import pandas as pd
import requests
import json
from datetime import datetime    # type: ignore 
from generateSchema import get_skyflow_params  # type: ignore

def batchLoad(directory, full_file, bearerToken, vault_id):
    batchCount = 0
    successful_records_count = 0  # Initialize the counter for successful records

    # Get Skyflow parameter details for run
    AccountId, Vault_URL, WorkspaceID, Vault_Name, Vault_Table_Name, Management_URL, user_id, Records_Batch_Size = get_skyflow_params(directory, bearerToken)

    # Initialize the records list
    records_list = []

    # Identify the columns to use for "fields" and the corresponding "tokens"
    field_columns = [col for col in full_file.columns if not ('token' in col.lower() or '_token' in col.lower())]
    token_column_map = {col: col + '_token' for col in field_columns}

    datetime1 = datetime.now()
    # Iterate over each row in the DataFrame
    for index, row in full_file.iterrows():
        fields = {}
        tokens = {}
        for column in field_columns:
            token_column = token_column_map[column]  # Get the corresponding token column name
            
            # Get field value and token value
            field_value = str(row[column]).strip() if isinstance(row[column], (int, float)) else str(row[column]).strip()
            token_value = row[token_column] if token_column in row and pd.notna(row[token_column]) else None
            
            # Add to fields
            fields[column] = field_value
            
            # Add to tokens only if the token exists
            if token_value:
                tokens[column] = str(token_value).strip()

        # Record structure with fields and tokens separated
        record = {
            "fields": fields,
            "tokens": tokens
        }
        records_list.append(record)
        #print(f"records list: {records_list}")

    # Set the headers
    headers = {
        'Authorization': f'Bearer {bearerToken}',
        'Content-Type': 'application/json'
    }

    # Create the URL for the Batch API inserts
    url = f'{Vault_URL}/v1/vaults/{vault_id}/{Vault_Table_Name}'

    # Function to send a batch of records
    def send_batch(batch):
        records_payload = {
            "records": batch,
            "tokenization": True,
            "continueOnError": False,
            "byot": "ENABLE"
        }
        #print(f"\nSending payload: {json.dumps(records_payload,indent=2)}")  #debug
        
        response = requests.post(url, headers=headers, data=json.dumps(records_payload))
        #print(f"\nresponse:\n{response.headers}")      #debug
        return response

    all_successful = True

    # Process the records in batches
    for i in range(0, len(records_list), Records_Batch_Size):
        batchCount += 1
        batch = records_list[i:i + Records_Batch_Size]
        response = send_batch(batch)

        # Check the response
        if response.status_code == 200:
            print(f"Batch record set #{batchCount} created.")
            successful_records_count += len(batch)  # Increment the counter by the size of the current batch
        else:
            print(f"Failed to create batch records. Status code: {response.status_code}")
            print(response.text)
            all_successful = False

    # Output the total number of successfully processed records
    datetime2 = datetime.now()
    print(f"Total successfully processed records: {successful_records_count}")
    print(f"Load elapsed time: {elapsed_time(datetime1, datetime2)} seconds\n")

    return all_successful

def elapsed_time(datetime1, datetime2):
    elapsed_time = datetime2 - datetime1            #elapsed
    elapsed_seconds = elapsed_time.total_seconds()    #convert to total seconds
    return f"{elapsed_seconds:.2f}"    #elapsed - two decimal places
