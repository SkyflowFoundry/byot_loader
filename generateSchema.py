import json
from datetime import datetime
from detect_data_type import detect_data_type  # type: ignore
from getUserID import getUserId  # type: ignore

def get_skyflow_params (directory, bearer_token):
    # get paramteters from JSON parameters file
    file_path = directory + '/' + 'byot_params.json'
    with open(file_path, 'r') as file:
        params = json.load(file)

    AccountId = params['AccountId']
    Vault_URL = params['Vault_URL']
    WorkspaceID = params['WorkspaceID']
    Vault_Name = params['Vault_Name']
    Vault_Table_Name = params['Vault_Table_Name']
    Management_URL = params['Management_URL']
    User_Email = params['User_Email']
    Records_Batch_Size = params['Records_Batch_Size']

    user_id = getUserId (AccountId, Management_URL, User_Email, bearer_token)

    return AccountId, Vault_URL, WorkspaceID, Vault_Name, Vault_Table_Name, Management_URL, user_id, Records_Batch_Size

# Generate skyflow email field definition
def generate_email_field(field_name):
    return {
  "name": field_name,
  "datatype": "DT_STRING",
  "isArray": False,
  "tags": [
    {
      "name": "skyflow.options.default_dlp_policy",
      "values": ["MASK"]
    },
    {
      "name": "skyflow.options.find_pattern",
      "values": ["^(.).*?(.)?@(.+)"]
    },
    {
      "name": "skyflow.options.replace_pattern",
      "values": ["$1******$2@$3"]
    },
    {
      "name": "skyflow.validation.regular_exp",
      "values": ["^$|^([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,})$"]
    },
    {
      "name": "skyflow.options.identifiability",
      "values": ["HIGH_IDENTIFIABILITY"]
    },
    {
      "name": "skyflow.options.operation",
      "values": ["EXACT_MATCH"]
    },
    {
      "name": "skyflow.options.default_token_policy",
      "values": ["DETERMINISTIC_FPT"]
    },
    {
      "name": "skyflow.options.format_preserving_regex",
      "values": ["^([a-z]{20})@([a-z]{10})\\.com$"]
    },
    {
      "name": "skyflow.options.configuration_tags",
      "values": ["NULLABLE"]
    },
    {
      "name": "skyflow.options.personal_information_type",
      "values": ["PII", "PHI"]
    },
    {
      "name": "skyflow.options.privacy_law",
      "values": ["GDPR", "CCPA", "HIPAA"]
    },
    {
      "name": "skyflow.options.sensitivity",
      "values": ["MEDIUM"]
    },
    {
      "name": "skyflow.options.data_type",
      "values": ["skyflow.PrimaryEmail"]
    },
    {
      "name": "skyflow.options.description",
      "values": ["Email Address of a person"]
    },
    {
      "name": "skyflow.options.display_name",
      "values": ["email"]
    }
        ]
    }

# Generate skyflow date field definition
def generate_date_field(field_name):
    return {
  "name": field_name,
  "datatype": "DT_STRING",
  "isArray": False,
  "tags": [
    {
      "name": "skyflow.options.default_dlp_policy",
      "values": ["MASK"]
    },
    {
      "name": "skyflow.options.find_pattern",
      "values": [
        "^$|([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1])))"
      ]
    },
    {
      "name": "skyflow.options.replace_pattern",
      "values": ["XXXX-${5}${6}"]
    },
    {
      "name": "skyflow.validation.regular_exp",
      "values": [
        "^$|([0-9]([0-9]([0-9][1-9]|[1-9]0)|[1-9]00)|[1-9]000)(-(0[1-9]|1[0-2])(-(0[1-9]|[1-2][0-9]|3[0-1])))"
      ]
    },
    {
      "name": "skyflow.options.identifiability",
      "values": ["MODERATE_IDENTIFIABILITY"]
    },
    {
      "name": "skyflow.options.operation",
      "values": ["EXACT_MATCH"]
    },
    {
      "name": "skyflow.options.default_token_policy",
      "values": ["DETERMINISTIC_UUID"]
    },
    {
      "name": "skyflow.options.personal_information_type",
      "values": ["PII", "PHI"]
    },
    {
      "name": "skyflow.options.privacy_law",
      "values": ["GDPR", "CCPA", "HIPAA"]
    },
    {
      "name": "skyflow.options.sensitivity",
      "values": ["MEDIUM"]
    },
    {
      "name": "skyflow.options.description",
      "values": ["Secure Date information"]
    }
  ]
    }

# Generate skyflow string field definition
def generate_string_field(field_name):
    return {
        "name": field_name,
        "datatype": "DT_STRING",
        "tags": [
                        {
                            "name": "skyflow.options.default_dlp_policy",
                            "values": [
                                "PLAIN_TEXT"
                            ]
                        },
                        {
                            "name": "skyflow.options.operation",
                            "values": [
                                "EXACT_MATCH"
                            ]
                        },
                        {
                            "name": "skyflow.options.default_token_policy",
                            "values": [
                                "NON_DETERMINISTIC_UUID"
                            ]
                        }            
        ]
    }

# Generate skyflow IP address field definition
def generate_ip_address(field_name):
    return {
          "name": field_name,
          "datatype": "DT_STRING",
          "isArray": False,
          "tags": [
            {
              "name": "skyflow.options.default_dlp_policy",
              "values": ["MASK"]
            },
            {
              "name": "skyflow.options.find_pattern",
              "values": ["(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.)(\\d{1,3})$"]
            },
            {
              "name": "skyflow.options.replace_pattern",
              "values": ["XXX.XXX.XXX.${2}"]
            },
            {
              "name": "skyflow.validation.regular_exp",
              "values": [
                "^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$",
                "^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$"
              ]
            },
            {
              "name": "skyflow.options.operation",
              "values": ["ALL_OP"]
            },
            {
              "name": "skyflow.options.default_token_policy",
              "values": ["RANDOM_TOKEN"]
            },
            {
              "name": "skyflow.options.display_name",
              "values": ["ip_address"]
            }
          ]
    }

# Generate int field definition
def generate_int_field(field_name):
    return {
        "name": field_name,
        "datatype": "DT_STRING",
        "tags": []
    }

# Generate skyflow email field definition
def generate_us_ssn_field(field_name):
    return {
          "name": field_name,
          "datatype": "DT_STRING",
          "isArray": False,
          "tags": [
            {
              "name": "skyflow.options.default_dlp_policy",
              "values": ["MASK"]
            },
            {
              "name": "skyflow.options.find_pattern",
              "values": ["^[0-9]{3}([- ])?[0-9]{2}([- ])?([0-9]{4})$"]
            },
            {
              "name": "skyflow.options.replace_pattern",
              "values": ["XXX${1}XX${2}${3}"]
            },
            {
              "name": "skyflow.validation.regular_exp",
              "values": ["^$|^([0-9]{3}-?[0-9]{2}-?[0-9]{4})$"]
            },
            {
              "name": "skyflow.options.identifiability",
              "values": ["HIGH_IDENTIFIABILITY"]
            },
            {
              "name": "skyflow.options.operation",
              "values": ["EXACT_MATCH"]
            },
            {
              "name": "skyflow.options.default_token_policy",
              "values": ["DETERMINISTIC_FPT"]
            },
            {
              "name": "skyflow.options.format_preserving_regex",
              "values": ["^[0-9]{3}-[0-9]{2}-([0-9]{4})$"]
            },
            {
              "name": "skyflow.options.personal_information_type",
              "values": ["PII", "PHI", "NPI"]
            },
            {
              "name": "skyflow.options.privacy_law",
              "values": ["GDPR", "CCPA", "HIPAA"]
            },
            {
              "name": "skyflow.options.sensitivity",
              "values": ["HIGH"]
            },
            {
              "name": "skyflow.options.data_type",
              "values": ["skyflow.SSN"]
            },
            {
              "name": "skyflow.options.description",
              "values": ["Social Security Number of a person"]
            },
            {
              "name": "skyflow.options.display_name",
              "values": ["Social Security Number"]
            }
          ]        
    }

def add_field(schema, field_name, field_type):
    # Skip fields that contain "_token" in the name
    if "_token" in field_name:
        return

    if field_type == "email":
        field_def = generate_email_field(field_name)
    elif field_type == "date":
        field_def = generate_date_field(field_name)
    elif field_type == "string":
        field_def = generate_string_field(field_name)
    elif field_type == "ip address":
        field_def = generate_ip_address(field_name)
    elif field_type == "int":
        field_def = generate_int_field(field_name)
    elif field_type == "us_ssn":
        field_def = generate_us_ssn_field(field_name)
    else:
        field_def = generate_string_field(field_name)  # if not found use string
        # raise ValueError(f"Unsupported field type: {field_type}")

    schema["vaultSchema"]["schemas"][0]["fields"].append(field_def)


def build_vault_schema(header_row, directory, bearer_token, sa1_id):
    # Get setup parameters for vault creation
    AccountId, Vault_URL, WorkspaceID, Vault_Name, Vault_Table_Name, Management_URL, user_id, Records_Batch_Size = get_skyflow_params(directory, bearer_token)

    now = datetime.now()
    time_string = now.strftime("%H%M%S")
    #Add HMS from time for unique vault and table names
    #Unique_Table_Name = Vault_Table_Name + str(time_string)
    Vault_Name = Vault_Name + str(time_string)

    today = datetime.today()
    formatted_date = today.strftime("%m/%d/%Y")
    vaultSchema = {
        "name": Vault_Name + str(time_string),
        "description": "Auto-created Vault from CSV File " + str(formatted_date),
        "vaultSchema": {
            "schemas": [
                {
                    "name": Vault_Table_Name,
                    "fields": []
                }
            ]
        },
        "workspaceID": WorkspaceID,
        "owners":[              # Add vault owners
            {
                "type":'USER',
                "ID":user_id    # Add user_id so vault visible in studio
            },
            {
                "type":'SERVICE_ACCOUNT',
                "ID":sa1_id    # Add SA _id
            }            
        ]        
    }

    # Appending csv fields to the JSON schema
    for column in header_row.columns:
        value = header_row[column].iloc[0]
        data_type = detect_data_type(value)
        add_field(vaultSchema, column, data_type.lower())
        #print(data_type.lower())

    #print(json.dumps(vaultSchema, indent=2))   # verify the generated schema
    return vaultSchema, AccountId

# header_row is a pandas DataFrame with column headers matching the fields of the CSV
# function usage: create_vault(header_row)
