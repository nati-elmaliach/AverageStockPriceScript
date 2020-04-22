import requests as req
# Why should we declare the key in here?
headers = {'Content-Type': 'application/json'}
api_key = "Your api key in here"

# validate the response was 200 OK


def validate_response(response):
    print(response)
    if response.status_code == 404:
        return None
    return response.json()


def http_get_request(api_url, payload=None):
    if payload:
        payload["token"] = api_key
    else:
        payload = {"token": api_key}

    response = req.get(api_url, params=payload, headers=headers)
    return validate_response(response)
