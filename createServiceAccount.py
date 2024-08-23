import requests
import json
import sys
from datetime import datetime
from get_bearer_token import getBearerToken, getSignedJWT_fromjson  # type: ignore

def generateSA(bearerToken, vaultID, AccountId):
    now = datetime.now()
    formatted_datetime = now.strftime("%m%d%Y-%H%M%S")  #used for: unique SA naming
    service_account_id = None
    bearerTokenVault = None
    creds = None

    # Set the Management URL for creating a service account
    url_create_sa = "https://manage.skyflowapis.com/v1/serviceAccounts"

    # Set the headers
    headers = {
        "Authorization": f"Bearer {bearerToken}",
        "Content-Type": "application/json",
        'X-SKYFLOW-ACCOUNT-ID': AccountId
    }

    # Set the data for creating a service account
    data_create_sa = {
        "resource": {
            "ID": vaultID,
            "type": "VAULT"
        },
        "serviceAccount": {
            "ID": vaultID,
            "name": f"serviceAccount@{AccountId}-{formatted_datetime}-skyflow.com",
            "displayName": f"SA-for-Record-Creation-in-AutoLoad-{formatted_datetime}",
            "description": "SA for vault admin"
        },
        "clientConfiguration": {
            "enforceContextID": False,  #CAA or not CAA
            "enforceSignedDataTokens": True
        }
    }
    #print(json.dumps(data_create_sa, indent=2))

    # POST request to create a service account
    response_create_sa = requests.post(url_create_sa, headers=headers, data=json.dumps(data_create_sa))

    # Check the response for creating a service account
    if response_create_sa.status_code == 200:
        print("Service Account created successfully.")
        response_data = response_create_sa.json()
        #print(f"Response data: \n {response_data}")

        #get the service account ID
        service_account_id =  response_data.get("clientID")
        if service_account_id:
            print(f"Service Account ID: {service_account_id}")
        else:
            print("No Service Account ID not found in: response.")
            sys.exit(1)

    else:
        print(f"Failed to create Service Account. Status code: {response_create_sa.status_code}")
        print(response_create_sa.text)
        sys.exit(1)

    #Create a Role and GET id
    role_id = getRoles(headers, vaultID)
    #assign the role to the Servcie Account
    status_code = saAssignRole(headers, vaultID, role_id, service_account_id)
    if status_code == 200:
        # call bearertoken generation 
        signedJWT, creds = getSignedJWT_fromjson(response_data)
        # print(f"signedJWT: {signedJWT}")
        #print(f"creds in cSA:\n   {creds}")
        bearerTokenVault = getBearerToken(signedJWT, creds)

        #print(f"bearerTokenVault:  \n {bearerTokenVault}")
        return bearerTokenVault  #pass back bearerToken for data load
    else:
        print(f"Failed to Assign to Service Account. Status code: {status_code}")


def getRoles(headers, vaultID):
    #URL and parameters - fetch ROLES
    url_get_roles = "https://manage.skyflowapis.com/v1/roles"
    params = {
        "resource.ID": vaultID,
        "resource.type": "VAULT"
    }

    #GET request ... fetch roles with query parameters
    response_get_roles = requests.get(url_get_roles, headers=headers, params=params)

    # Check the response for roles
    if response_get_roles.status_code == 200:
        print("Roles fetched successfully.")
        data = response_get_roles.json()
        roles = data.get('roles', [])

        #output roles info
        if roles:
            for role in roles:
                role_id = role.get('ID')
                role_name = role.get('definition', {}).get('name')
                resource_type = role.get('resource', {}).get('type')
                if role_name == 'VAULT_OWNER':
                    #print(f"Role ID: {role_id}, Role Name: {role_name}, Resource Type: {resource_type}")
                    return role_id
        else:
            print(f"No roles found for the specified resource ID and resource type.")
    else:
        print(f"Failed to fetch roles. Status code: {response_get_roles.status_code}")
        #print(response_get_roles.text)

def saAssignRole(headers, vaultID, role_id, service_account_id):
    #Set the URL for assigning a role to the service account
    url_assign_role = "https://manage.skyflowapis.com/v1/roles/assign"

    #Set the data for assigning a role
    data_assign_role = {
        "ID": role_id,      #inbound value to function
        "members": [
            {
                "ID": service_account_id,    #inbound value to function
                "type": "SERVICE_ACCOUNT"
            }
        ]
    }

    #send the POST request to assign the role
    response_assign_role = requests.post(url_assign_role, headers=headers, data=json.dumps(data_assign_role))

    # Check the response
    if response_assign_role.status_code == 200:
        print("Role assigned to the Service Account successfully.")
        print(response_assign_role.json())
        print(f"Status code for SA Assign: {response_assign_role.status_code}")
        return response_assign_role.status_code
    else:
        print(f"Failed to assign role to the Service Account. Status code: {response_assign_role.status_code}")
        print(response_assign_role.text)

# Call the function to generate the service account and fetch roles - testing
# generateSA(bearerToken, vaultID, AccountId)
