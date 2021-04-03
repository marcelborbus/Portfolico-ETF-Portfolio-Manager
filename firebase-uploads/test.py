import requests
from requests.structures import CaseInsensitiveDict

# url = "http://127.0.0.1:8080/" 
url = "https://europe-west3-genuine-airfoil-309308.cloudfunctions.net/optimizer"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

data = """
{
    "countries": {
        "United States of America (the)": 0.2,
        "Argentina": 0.0,
        "Canada": 0.1,
        "Chile": 0.0,
        "China": 0.2,
        "Denmark": 0.1,
        "France": 0.2,
        "India": 0.1,
        "Ireland": 0.0,
        "Israel": 0.0,
        "Italy": 0.1
    },
    "industries": {
        "Diversified Consumer Services": 0.2,
        "Hotels, Restaurants & Leisure": 0.3,
        "IT Services": 0.4,
        "Internet & Direct Marketing Retail": 0.1,
        "Life Sciences Tools & Services": 0.0
    }
}
"""


resp = requests.post(url, headers=headers, data=data)



print(resp.status_code)
print(resp.text)
