from request_manager import process_request
import json

# py -3.8 main.py

def main():
    with open('prefs.json', "rb") as f:
        user_req = f.read()

    result = json.loads(process_request(user_req))

    print('result:', result['result'])
    print('deviance:', result['deviance'])
    print('status_code:', result['status_code'])
    # print('estimate:', result['estimate'])

main()