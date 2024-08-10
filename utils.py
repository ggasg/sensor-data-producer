import requests

def get_location():
    # May need to switch to a proper api-key based approach
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    return data