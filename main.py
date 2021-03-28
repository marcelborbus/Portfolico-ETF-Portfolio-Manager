from request_manager import process_request
import json

# py -3.8 main.py

def main():
    with open('prefs.json', "rb") as f:
        user_req = f.read()

    result = json.loads(process_request(user_req))

    print()
    print('result', result['result'])
    print('error:', result['error'])
    print()

main()