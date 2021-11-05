import requests
import json
from requests.auth import HTTPBasicAuth
res = requests.get('https://api.quickbutik.com/v1/products', auth=HTTPBasicAuth('9PLVHsF#aYYI!VC5snz0tBml5lBVNZ7Z', '9PLVHsF#aYYI!VC5snz0tBml5lBVNZ7Z'))

print(res.content)