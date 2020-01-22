import json


def generate_response(text):
    payload = {}
    payload['google'] = {}
    payload['google']["expectUserResponse"] = False
    response_data = {}
    response_data['payload'] = payload
    response_data['fulfillmentText'] = text
    return json.dumps(response_data)
