import json
import jwt
import requests
import time

def getSignedJWT_fromfile(credsFile):
   # credsFile is the filepath to your credentials.json file

    fd = open(credsFile)
    #credsFile
    creds = json.load(fd)
    fd.close()

   # Create the claims object with the data in the creds object
    claims = {
       "iss": creds["clientID"],
       "key": creds["keyID"],
       "aud": creds["tokenURI"],
       "exp": int(time.time()) + (3600), # JWT expires in Now + 6 hours
       "sub": creds["clientID"],
   }
   # Sign the claims object with the private key contained in the creds object
    signedJWT = jwt.encode(claims, creds["privateKey"], algorithm='RS256')
    return signedJWT, creds, creds["clientID"]


def getSignedJWT_fromjson(creds):
    #Generate signedJWT from creds json passed in the function
    #print(f"Creds: \n {creds}")     #debug
   # Create the claims object with the data in the creds object
    claims = {
       "iss": creds["clientID"],
       "key": creds["keyID"],
       "aud": creds["tokenURI"],
       "exp": int(time.time()) + (3600), # JWT expires in Now + 6 hours
       "sub": creds["clientID"],
   }
    #print(f"creds: \n {creds}")
   #sign claims object with the private key contained in the creds object
    signedJWT = jwt.encode(claims, creds["privateKey"], algorithm='RS256')
    return signedJWT, creds

def getBearerToken(signedJWT, creds):
   # Request body parameters
    body = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': signedJWT,
        }
   # Request URI (== https://api.skylfow.dev/v1/auth/sa/oauth/token)
    tokenURI = creds["tokenURI"]

   # Send the POST request
    r = requests.post(tokenURI, json=body)
    #print(f"tokenURL: \n {tokenURI} \n payload: \n {body}")

    #modification to get just the accessToken and return that.
    response_json   = json.loads(r.text)
    #print(response_json.get("accessToken"))
    #print(f"response_json: \n {response_json}")
    bearerToken = response_json.get("accessToken")
    #return r
    #return r.text
    return bearerToken
