import requests
import sys

def getUserId (AccountId, Management_URL, User_Email, bearer_token):

    # Define the URL and the specific query parameters
    url = Management_URL + '/v1/users'
    params = {
        'accountID': AccountId,
        'filterOps.email': User_Email
    }

    # Set the headers
    headers = {
        'X-SKYFLOW-ACCOUNT-ID': AccountId,
        'Accept': 'application/json',
        'Authorization': f'Bearer {bearer_token}'
    }

    # Make the call
    response = requests.get(url, headers=headers, params=params)

    # Check response success
    if response.status_code == 200:
        response_json = response.json()
        # Check there is at least one user in the response and get the ID
        if 'users' in response_json and len(response_json['users']) > 0:
            user_id = response_json['users'][0]['ID']
            #print(f"User ID: {user_id}")     #debug
            return user_id
        else:
            print("No users found in the response.")
            sys.exit(1)
    else:
        print(f"Failed to fetch user data. Status code: {response.status_code}")
        print(response.text)

