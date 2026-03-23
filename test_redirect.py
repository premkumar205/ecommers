import requests

url = "http://127.0.0.1:8000/api/image?id=7&prompt=A%20professiond%20atmosphere.%20and%20sophisticated"
try:
    response = requests.get(url, allow_redirects=False)
    print(f"Status: {response.status_code}")
    if "Location" in response.headers:
        print(f"Redirect URL: {response.headers['Location']}")
    else:
        print("No Location header found.")
except Exception as e:
    print(f"Error: {e}")
